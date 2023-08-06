import dataclasses
import enum
from typing import Any, List, Optional

__all__ = [
    "OptionModifier",
]


class OptionModifier(enum.Enum):
    NoModifier = "no_modifier"
    ConsumeRest = "consume_rest"


@dataclasses.dataclass
class Option:
    name: str
    value: str
    modifier: OptionModifier = OptionModifier.NoModifier


class Options:
    def __init__(self, options: List[Option] = None):
        if options is None:
            self.options = []
        else:
            self.options = options

    def __getattr__(self, name: str) -> Optional[str]:
        option = self.get(name)

        if option:
            return option.value

    def get(self, name: str) -> Option:
        for option in self.options:
            if option.name == name:
                return option

    def has_option(self, name: str) -> Optional[int]:
        if self.get(name):
            return True

        return False

    def add(
        self,
        name: str,
        default: Any = None,
        modifier: OptionModifier = OptionModifier.NoModifier,
        append: bool = False,
    ):
        option = self.has_option(name)

        if not option:
            option_args = []
            option_args.append(name)
            option_args.append(default)
            option_args.append(modifier)

            if not append:
                self.options.insert(0, Option(*option_args))
            else:
                self.options.append(Option(*option_args))
