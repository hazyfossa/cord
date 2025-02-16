from dataclasses import dataclass
from subprocess import PIPE, Popen
from typing import IO, BinaryIO, cast

from pyoci.runtime.client import errors


# - default with encode=False is only for documentation
# (i.e. showing default values within a container runtime)
# - default with encode=True is a regular python default
def default(value, encode=False):
    if encode:
        return value

    return None


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
    def __init__(self, path: str, global_args: list[str], setpgid: bool = False):
        self.executable_path = path
        self.__global_args__ = global_args
        self.__setpgid = setpgid

    def _run_raw(
        self,
        *args,
        stdin: int | IO | None = None,
        stdout: int | IO | None = PIPE,
        wait: bool = True,
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

        if wait:
            process.wait()

        return process

    def _run(
        self,
        *args,
        stdin: int | IO | None = None,
        **kwargs,
    ) -> BinaryIO:
        process = self._run_raw(*args, stdin=stdin, **kwargs)
        errors.handle(process)
        return cast(BinaryIO, process.stdout)
