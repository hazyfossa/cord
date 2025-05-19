from pathlib import Path
from subprocess import PIPE, Popen
from typing import IO, BinaryIO, Callable, cast

type CLIArgs = list[str]

type SubprocessIO = int | IO | None


class CLIWrapperBase:
    def __init__(
        self,
        path: str | Path,
        global_args: CLIArgs,
        error_handler: Callable[[Popen], None] | None = None,
        setpgid: bool = False,
    ):
        self.executable_path = str(path)

        self._error_handler = error_handler
        self._global_args = global_args
        self._setpgid = setpgid

    def _run_raw(
        self,
        *args,
        stdin: SubprocessIO = None,
        stdout: SubprocessIO = PIPE,
        stderr: SubprocessIO = PIPE,
        **kwargs,
    ):
        process = Popen(
            [self.executable_path, *self._global_args, *args],
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            process_group=0 if self._setpgid else None,
            **kwargs,
        )

        return process

    def _run(
        self,
        *args,
        stdin: int | IO | None = None,
        **kwargs,
    ) -> BinaryIO:
        process = self._run_raw(*args, stdin=stdin, **kwargs)

        process.wait()

        if self._error_handler:
            self._error_handler(process)

        return cast(BinaryIO, process.stdout)
