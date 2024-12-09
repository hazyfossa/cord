from abc import ABC, abstractmethod
from typing import Any, Self

# Yes, this isn't DRY at all, however it's easy to read and should be performant enough
# TODO: Revisit. Maybe use a bit of type-parsing magic?

# TODO initialize CLIArguments as a descriptor once, not on each function invocation, and bind to that descriptor


class CLIArgument(ABC):
    def __init__(self, string: str) -> None:
        self.string = string

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> str | None: ...


class flag(CLIArgument):
    def __call__(self, value: bool | None) -> str | None:
        if value:
            return self.string


class option(CLIArgument):
    def __call__(self, value: Any) -> str | None:
        return self.string.format(value)


class CLIArguments:
    def __init__(self) -> None:
        self.store = []

    def __truediv__(self, arg: str | None) -> Self:
        if arg is not None:
            self.store.append(arg)

        return self

    @property
    def list(self) -> list[str]:
        return self.store
