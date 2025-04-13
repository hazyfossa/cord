from pathlib import Path
from subprocess import PIPE, Popen
from typing import IO, BinaryIO, Callable, cast


class CLIWrapperBase:
    def __init__(
        self,
        path: str | Path,
        global_args: list[str],
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
        stdin: int | IO | None = None,
        stdout: int | IO | None = PIPE,
        **kwargs,
    ):
        process = Popen(
            [self.executable_path, *self._global_args, *args],
            stdin=stdin,
            stdout=stdout,
            stderr=PIPE,  # TODO: errors without stderr
            process_group=0 if self._setpgid else None,
            **kwargs,
        )

        process.wait()

        if self._error_handler:
            self._error_handler(process)

        return process

    def _run(
        self,
        *args,
        stdin: int | IO | None = None,
        **kwargs,
    ) -> BinaryIO:
        process = self._run_raw(*args, stdin=stdin, **kwargs)
        return cast(BinaryIO, process.stdout)
