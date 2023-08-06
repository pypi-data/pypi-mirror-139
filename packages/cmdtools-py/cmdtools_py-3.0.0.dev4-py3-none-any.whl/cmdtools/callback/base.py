from __future__ import annotations

import inspect
import typing
from typing import Any, Callable, Dict, Optional, Union

from cmdtools.callback.option import OptionModifier, Options
from cmdtools.errors import NotEnoughArgumentError

if typing.TYPE_CHECKING:
    from cmdtools import Cmd

__all__ = [
    "Attributes",
    "Context",
    "ErrorContext",
    "Callback",
    "ErrorCallback",
    "callback_init",
    "add_option",
]


class Attributes:
    def __init__(self, attrs: Dict[str, Any] = None):
        if attrs is None:
            self.attrs = {}
        else:
            self.attrs = attrs

    def __getattr__(self, name: str) -> Optional[str]:
        return self.attrs.get(name)


class BaseContext:
    def __init__(self, command: Cmd, attrs: Union[Attributes, Dict[str, Any]] = None):
        self.command = command

        if isinstance(attrs, Attributes):
            self.attrs = attrs
        elif isinstance(attrs, dict):
            self.attrs = Attributes(attrs)
        else:
            self.attrs = Attributes()


class Context(BaseContext):
    def __init__(
        self,
        command: Cmd,
        options: Options = None,
        attrs: Union[Attributes, Dict[str, Any]] = None,
    ):
        if isinstance(options, Options):
            self.options = options
        elif isinstance(options, dict):
            self.options = Options(options)
        else:
            self.options = Options()

        super().__init__(command, attrs)

        for idx, option in enumerate(self.options.options):
            if idx < len(self.command.args):
                if option.modifier is OptionModifier.ConsumeRest:
                    option.value = " ".join(self.command.args[idx:])
                else:
                    option.value = self.command.args[idx]

            if option.value is None:
                raise NotEnoughArgumentError(
                    f"Not enough argument for option: {option.name}", option.name
                )

            self.options.options[idx] = option


class ErrorContext(BaseContext):
    def __init__(self, command: Cmd, error: Exception, attrs: Attributes = None):
        self.error = error
        super().__init__(command, attrs)


class BaseCallback:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @property
    def is_coroutine(self):
        return inspect.iscoroutinefunction(self.func)


class ErrorCallback(BaseCallback):
    def make_context(self, command: Cmd, error: Exception, attrs: Attributes = None):
        return ErrorContext(command, error, attrs)


class Callback(BaseCallback):
    def __init__(self, func: Callable):
        self.options = Options()
        self.errcall = None
        super().__init__(func)

    def make_context(self, command: Cmd, attrs: Attributes = None) -> Context:
        return Context(command, self.options, attrs)

    def error(self, func: Callable) -> ErrorCallback:
        self.errcall = ErrorCallback(func)
        return self.errcall


def callback_init(func: Callable) -> Callback:
    return Callback(func)


def add_option(
    name: str,
    *,
    default: Any = None,
    modifier: OptionModifier = OptionModifier.NoModifier,
):
    def decorator(obj):
        if isinstance(obj, Callback):
            obj.options.add(name, default, modifier)
        elif isinstance(obj, Callable):
            obj = Callback(obj)
            obj.options.add(name, default, modifier)
        else:
            raise TypeError(f"Cannot add option to object {obj!r}")

        return obj

    return decorator
