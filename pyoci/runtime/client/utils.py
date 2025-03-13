from dataclasses import dataclass
from pathlib import Path
from subprocess import PIPE, Popen
from typing import IO, BinaryIO, cast

from pyoci.runtime.client import errors


@dataclass
class OpenIO:
    stdin: BinaryIO
    stdout: BinaryIO
    stderr: BinaryIO

    @property
    def as_tuple(self):
        return (self.stdin, self.stdout, self.stderr)

    def close(self) -> None:
        map(lambda x: x.close(), self.as_tuple)


class CLIWrapperBase:
    def __init__(self, path: str | Path, global_args: list[str], setpgid: bool = False):
        self.executable_path = str(path)
        self.__global_args__ = global_args
        self.__setpgid = setpgid

    def _run_raw(
        self,
        *args,
        stdin: int | IO | None = None,
        stdout: int | IO | None = PIPE,
        **kwargs,
    ):
        process = Popen(
            [self.executable_path, *self.__global_args__, *args],
            stdin=stdin,
            stdout=stdout,
            stderr=PIPE,  # TODO: errors without stderr
            process_group=0 if self.__setpgid else None,
            **kwargs,
        )

        process.wait()
        errors.handle(process)

        return process

    def _run(
        self,
        *args,
        stdin: int | IO | None = None,
        **kwargs,
    ) -> BinaryIO:
        process = self._run_raw(*args, stdin=stdin, **kwargs)
        return cast(BinaryIO, process.stdout)
