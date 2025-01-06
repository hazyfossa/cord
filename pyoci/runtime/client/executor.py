from subprocess import Popen
from pyoci.runtime.client.io import IODescriptor, OpenIO
from pyoci.runtime.client import errors


# TODO: maybe it's possible to implement more efficent handling of file descriptors than with
# python's subprocess pipe handling
class RuntimeExecutor:
    def __init__(
        self, path: str, global_args: list[str], raise_errors: bool = True
    ) -> None:
        self.path = path
        self.global_args = global_args
        self.raise_errors = raise_errors

    def run(self, *args, **kwargs) -> OpenIO:
        # TODO: combine_stderr
        # TODO: what about interactive mode?
        io = IODescriptor.piped()

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

        return OpenIO(p.stdin, p.stdout, p.stderr)  # type: ignore # these are never None

    def run_unary(self, *args):
        io = self.run(*args)
        stdout = io.stdout
        assert stdout is not None
        return stdout.read()
