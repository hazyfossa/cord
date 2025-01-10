from subprocess import Popen
from typing import IO

from pyoci.runtime.client import errors
from pyoci.runtime.client.io import IODescriptor, OpenIO


#! DEPRECATED


# TODO: maybe it's possible to implement more efficent handling of file descriptors than with
# python's subprocess pipe handling
# TODO: Is reaping an issue in python?
class RuntimeExecutor:
    def __init__(
        self,
        path: str,
        global_args: list[str],
        raise_errors: bool = True,
        setpgid: bool = False,
    ) -> None:
        self.path = path
        self.global_args = global_args
        self.raise_errors = raise_errors
        self.setpgid = setpgid

    def run(self, *args, io: OpenIO | None = None, **kwargs) -> OpenIO:
        # TODO: combine_stderr # NOTE: this and a bit more is possible, if we separate error io from process io
        # TODO: what about interactive mode?

        # TODO: sanitize env (remove NOTIFY_SOCKET)
        _io = io or IODescriptor.piped()

        p = Popen(
            [self.path, *self.global_args, *args],
            stdin=_io.stdin,
            stdout=_io.stdout,
            stderr=_io.stderr,
            process_group=0 if self.setpgid else None,
            **kwargs,
        )

        ret = p.wait()

        if ret != 0 and self.raise_errors:
            errors.handle(p.stderr)

        return OpenIO(p.stdin, p.stdout, p.stderr)  # type: ignore # these are never None

    def run_unary(self, *args, **kwargs):
        io = self.run(*args, **kwargs)
        stdout = io.stdout
        return stdout.read()
