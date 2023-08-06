import inspect
from typing import Any, Callable, Dict, List, Optional, Union

from cmdtools import Cmd, Executor, NotFoundError
from cmdtools.callback import Attributes, Callback, ErrorCallback
from cmdtools.callback.option import OptionModifier

__all__ = ["Command", "Group"]

class BaseCommand:
    _callback: Optional[Callback]

    def __init__(self, name: str):
        self.name = name
        self._callback = None

    @property
    def callback(self) -> Optional[Callback]:
        if not isinstance(self._callback, Callback):
            func: Callable = getattr(self, self.name, None)
            errfunc: Callable = getattr(self, "error_" + self.name, None)

            if inspect.ismethod(func):
                self._callback = Callback(func)
                if errfunc:
                    self._callback.errcall = ErrorCallback(errfunc)
                return self._callback
        else:
            return self._callback

    def add_option(
        self,
        name: str,
        *,
        default: Any = None,
        modifier: OptionModifier = OptionModifier.NoModifier,
    ):
        self.callback.options.add(name, default, modifier, append=True)


class Command(BaseCommand):
    def __init__(self, name: str, aliases: List[str] = None):
        if aliases is None:
            aliases = []
        self._aliases = aliases
        super().__init__(name)

    @property
    def aliases(self) -> List[str]:
        if self._aliases:
            return self._aliases

        return getattr(self, "__aliases__", [])


class GroupWrapper(Command):
    def __init__(self, name: str, aliases: List[str] = None):
        super().__init__(name, aliases)

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    @property
    def error_callback(self) -> Optional[ErrorCallback]:
        return self.callback.errcall


class Group:
    def __init__(self, name: str, commands: List[Command] = None):
        self.name = name

        if commands is None:
            commands = []

        self.commands = []

    def command(self, name: str = None, *, aliases: List[str] = None):
        if aliases is None:
            aliases = []

        def decorator(obj):
            if inspect.isclass(obj) and Command in inspect.getmro(obj):
                self.commands.append(obj())
            else:
                wrapper = GroupWrapper(name or obj.__name__, aliases)
                wrapper._callback = Callback(obj)
                self.commands.append(wrapper)

                return wrapper
            return obj

        return decorator

    async def run(
        self, command: Cmd, *, attrs: Union[Attributes, Dict[str, Any]] = None
    ):
        if attrs is None:
            attrs = {}

        for cmd in self.commands:
            if cmd.name == command.name or command.name in cmd.aliases:
                executor = Executor(command, cmd.callback, attrs=attrs)

                if cmd.callback.is_coroutine:
                    return await executor.exec_coro()

                return executor.exec()

        raise NotFoundError(f"Command not found: {command.name}", command.name)
