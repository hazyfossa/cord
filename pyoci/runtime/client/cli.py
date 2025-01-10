from abc import ABC, abstractmethod
from typing import Any, Callable, Literal, Self, overload


# Yes, this isn't DRY at all, however it's easy to read and should be performant enough
# TODO: Revisit. Maybe use a bit of type-parsing magic?

# TODO initialize CLIArguments as a descriptor once, not on each function invocation, and bind to that descriptor


class CLIArgument(ABC):
    def __init__(self, string: str) -> None:
        self.string = string
        self.partial = True

    # @cached_property
    # def pythonic(self) -> str:
    #     return self.string.strip("-").replace("-", "_")

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> str | None: ...


class _flag(CLIArgument):
    def __call__(self, value: bool | None) -> str | None:
        if value:
            return self.string


flag = _flag  # This is done purely so that the colors in an IDE are different


class option(CLIArgument):
    def __call__(self, value: Any) -> str | None:
        if value is not None:
            return self.string + f"={value}"


class CLIArguments:
    def __init__(self) -> None:
        self.store = []

    def __truediv__(self, arg: str | CLIArgument | None) -> Self:
        if arg is not None:
            self.store.append(arg)

        return self

    @property
    def list(self) -> list[str]:
        return self.store


# - default with encode=False is only for documentation
# (i.e. showing default values within a container runtime)
# - default with encode=True is a regular python default
def default(value, encode=False):
    if encode:
        return value

    return None
