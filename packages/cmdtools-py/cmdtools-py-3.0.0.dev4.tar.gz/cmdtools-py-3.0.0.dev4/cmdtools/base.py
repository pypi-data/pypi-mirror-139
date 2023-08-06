from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from cmdtools import utils
from cmdtools.callback import Attributes, Callback

__all__ = ["Cmd", "Executor", "execute"]


class Cmd:
    def __init__(self, text: str, prefix: str = "/"):
        self.text = text
        self.prefix = utils.string.PrefixChecker(text, prefix)

    @property
    def _args(self) -> Optional[List[str]]:
        return utils.string.splitargs(self.prefix.strip_prefix)

    @property
    def args(self) -> Optional[List[str]]:
        if len(self._args) > 1:
            return self._args[1:]

        return []

    @property
    def name(self) -> Optional[str]:
        if len(self._args) >= 1:
            return self._args[0]


class Executor:
    def __init__(
        self,
        command: Cmd,
        callback: Callback,
        *,
        attrs: Union[Attributes, Dict[str, Any]] = None,
    ):
        self.command = command
        if not isinstance(attrs, Attributes):
            if isinstance(attrs, dict):
                self.attrs = Attributes(attrs)
            else:
                self.attrs = Attributes()
        else:
            self.attrs = attrs

        if not isinstance(callback, Callback):
            raise TypeError(f"{callback!r} is not a Callback type!")
        self.callback = callback

        if self.callback.errcall:
            if self.callback.is_coroutine:
                if not self.callback.errcal.is_coroutine:
                    raise TypeError(
                        "Error callback should be a coroutine function if callback is coroutine"
                    )
            elif self.callback.errcall.is_coroutine:
                if not self.callback.is_coroutine:
                    raise TypeError(
                        "Error callback cannot be a coroutine function if callback is not a coroutine function"
                    )

    def exec(self) -> Optional[Any]:
        result = None

        try:
            context = self.callback.make_context(self.command, self.attrs)
            result = self.callback(context)
        except Exception as exception:
            if self.callback.errcall:
                error_context = self.callback.errcall.make_context(
                    self.command, exception, self.attrs
                )
                result = self.callback.errcall(error_context)
            else:
                raise exception

        return result

    async def exec_coro(self) -> Optional[Any]:
        result = None

        try:
            context = self.callback.make_context(self.command, self.attrs)
            result = await self.callback(context)
        except Exception as exception:
            if self.callback.errcall:
                error_context = self.callback.errcall.make_context(
                    self.command, exception, self.attrs
                )
                result = await self.callback.errcall(error_context)
            else:
                raise exception

        return result


async def execute(
    command: Cmd,
    callback: Callback,
    *,
    attrs: Union[Attributes, Dict[str, Any]] = None,
):
    executor = Executor(command, callback, attrs=attrs)

    if callback.is_coroutine:
        return await executor.exec_coro()

    return executor.exec()
