import os
import sys
from dataclasses import dataclass
from subprocess import DEVNULL, PIPE, STDOUT, Popen
from typing import Callable, TypeAlias

from pyoci.runtime.client import errors

Fd: TypeAlias = int


@dataclass
class IO:
    stdin: Fd = DEVNULL
    stdout: Fd = DEVNULL
    stderr: Fd = DEVNULL

    @property
    def as_tuple(self):
        return (self.stdin, self.stdout, self.stderr)

    @classmethod
    def current(cls):
        return cls(
            sys.stdin.fileno(),
            sys.stdout.fileno(),
            sys.stderr.fileno(),
        )

    @classmethod
    def piped(cls, combine_stderr: bool = False):
        return cls(stdin=PIPE, stdout=PIPE, stderr=STDOUT if combine_stderr else PIPE)

    def use_as_current(self) -> Callable[[], None]:
        override = IOOverride(previous=IO.current(), with_=self)
        return override.revert


class IOOverride:
    def __init__(self, previous: IO, with_: IO) -> None:
        self.original = previous.as_tuple
        self.new = with_.as_tuple

    def apply(self):
        [os.dup2(a, b) for a, b in zip(self.original, self.new)]

    def revert(self):
        [os.dup2(a, b) for a, b in zip(self.new, self.original)]

    def __enter__(self):
        self.apply()

    def __exit__(self):
        self.revert()


class RuntimeExecutor:
    def __init__(
        self, path: str, global_args: list[str], raise_errors: bool = True
    ) -> None:
        self.path = path
        self.global_args = global_args
        self.raise_errors = raise_errors

    def run(self, *args, **kwargs):
        io = IO.piped()

        p = Popen(
            [self.path, *self.global_args, *args],
            stdin=io.stdin,
            stdout=io.stdout,
            stderr=io.stderr,
            **kwargs,
        )

        ret = p.wait()

        if ret != 0 and self.raise_errors:
            errors.handle(p.stderr)

        return p.stdout

    def run_unary(self, *args):
        stdout = self.run(*args)
        assert stdout is not None
        return stdout.read()
