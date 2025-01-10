from subprocess import Popen
from pyoci.runtime.client.io import IODescriptor, OpenIO
from pyoci.runtime.client import errors


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

    def run(self, *args, **kwargs) -> OpenIO:
        # TODO: combine_stderr
        # TODO: what about interactive mode?

        # TODO: sanitize env (remove NOTIFY_SOCKET)
        io = IODescriptor.piped()

        p = Popen(
            [self.path, *self.global_args, *args],
            stdin=io.stdin,
            stdout=io.stdout,
            stderr=io.stderr,
            process_group=0 if self.setpgid else None,
            **kwargs,
        )

        ret = p.wait()

        if ret != 0 and self.raise_errors:
            errors.handle(p.stderr)

        return OpenIO(p.stdin, p.stdout, p.stderr)  # type: ignore # these are never None

    def run_unary(self, *args):
        io = self.run(*args)
        stdout = io.stdout
        return stdout.read()
