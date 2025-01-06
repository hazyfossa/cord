import os
import sys
from asyncio.subprocess import create_subprocess_exec
from dataclasses import dataclass
from subprocess import DEVNULL, PIPE
from typing import IO as IOType
from typing import Any

from pyoci.runtime.client import errors


@dataclass
class IO:
    stdin: IOType[Any] | int | None = DEVNULL
    stdout: IOType[Any] | int | None = DEVNULL
    stderr: IOType[Any] | int | None = DEVNULL

    @classmethod
    def current(cls):
        return cls(sys.stdin, sys.stdout, sys.stderr)


class AsyncRuntimeExecutor:
    def __init__(
        self, path: str, global_args: list[str], raise_errors: bool = True
    ) -> None:
        self.path = path
        self.global_args = global_args
        self.raise_errors = raise_errors

    async def run(self, *args, io: IO | None = None):
        io = io or IO(stderr=PIPE)

        cmd = (
            self.path,
            *self.global_args,
            *args,
        )

        p = await create_subprocess_exec(
            *cmd,
            stdin=io.stdin,
            stdout=io.stdout,
            stderr=io.stderr,
        )

        ret = await p.wait()

        if ret != 0 and self.raise_errors:
            await errors.handle(p.stderr)

        return p.stdout

    async def run_unary(self, *args):
        stdout = await self.run(*args)
        assert stdout is not None
        return await stdout.read()
