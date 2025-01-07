from functools import cached_property
import os
import sys
from dataclasses import dataclass
from subprocess import DEVNULL, PIPE, STDOUT
from typing import IO as IOType, BinaryIO, Literal
from typing import Any, Callable, TypeAlias

Fd: TypeAlias = int


@dataclass
class IODescriptor:
    stdin: Fd = DEVNULL  # TODO: won't stdin=DEVNULL cause problems?
    stdout: Fd = DEVNULL
    stderr: Fd = DEVNULL

    def open(
        self, mode: Literal["rb", "wb"] = "rb"
    ) -> "OpenIO":  # TODO: Other binary modes?
        return OpenIO(*[open(i, mode) for i in self.as_tuple])

    @classmethod
    def from_open_io(cls, open_io: "OpenIO"):
        return cls(
            open_io.stdin.fileno(),
            open_io.stdout.fileno(),
            open_io.stderr.fileno(),
        )

    @classmethod
    def current(cls):
        return cls(0, 1, 2)

    @classmethod
    def piped(cls, combine_stderr: bool = False):
        return cls(stdin=PIPE, stdout=PIPE, stderr=STDOUT if combine_stderr else PIPE)

    @property
    def as_tuple(self):
        return (self.stdin, self.stdout, self.stderr)

    def use_as_current(self) -> Callable[[], None]:
        override = IOOverride(previous=IODescriptor.current(), with_=self)
        return override.revert


class IOOverride:  #! TODO: Doesn't work
    def __init__(self, previous: IODescriptor, with_: IODescriptor) -> None:
        self.original = previous.as_tuple
        self.new = with_.as_tuple

    def apply(self) -> None:
        [os.dup2(a, b) for a, b in zip(self.original, self.new)]

    def revert(self) -> None:
        [os.dup2(a, b) for a, b in zip(self.new, self.original)]

    def __enter__(self):
        self.apply()

    def __exit__(self):
        self.revert()


@dataclass
class OpenIO:
    stdin: BinaryIO
    stdout: BinaryIO
    stderr: BinaryIO

    @cached_property
    def descriptor(self) -> IODescriptor:
        return IODescriptor.from_open_io(self)

    @property
    def as_tuple(self):
        return (self.stdin, self.stdout, self.stderr)

    def use_as_current(self) -> Callable[[], None]:  #! TODO: Doesn't work
        raise NotImplementedError
        return self.descriptor.use_as_current()

    def close(self) -> None:
        map(lambda x: x.close(), self.as_tuple)
