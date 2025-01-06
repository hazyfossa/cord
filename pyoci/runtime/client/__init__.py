from functools import cached_property
from typing import Literal

from msgspec import json

from pyoci.runtime.client.cli import (
    CLIArguments,
    default,
    flag,
    option,
)
from pyoci.runtime.client.executor import IO, RuntimeExecutor
from pyoci.runtime.client.spec.features import Features
from pyoci.runtime.client.specific.runc import State


# TODO: Implement a pure-oci runtime interface, just in case
# TODO: cleanly support differences between runc and crun
class Runc:
    def __init__(
        self,
        path: str,
        handle_errors: bool = True,
        debug: bool | None = default(False),
        log: str | None = default("/dev/stderr"),
        log_format: Literal["text", "json"] | None = default("text"),
        root: str | None = default("/run/user/1000//runc"),
        systemd_cgroup: bool | None = default(False),
        rootless: bool | Literal["auto"] | None = default("auto"),
    ):
        path = str(path)

        if handle_errors:
            if log or log_format:
                raise ValueError(  # TODO: is this an appropriate Exception type?
                    "Setting log or log_format is not supported when using handle_errors"
                )

            log_format = "json"

        self.__global_args__ = (
            CLIArguments()
            / flag("--debug")(debug)
            / option("--log")(log)
            / option("--log-format")(log_format)
            / option("--root")(root)
            / flag("--systemd-cgroup")(systemd_cgroup)
            / option("--rootless")(
                str(rootless).lower() if rootless is not None else None
            )
        ).list

        executor = RuntimeExecutor(path, self.__global_args__)
        self._run = executor.run
        self._run_unary = executor.run_unary

    def create(
        self,
        id: str,
        bundle: str,
        io: IO = default(lambda: IO.current(), factory=True),
        console_socket: str | None = None,
        pid_file: str | None = None,
        no_pivot: bool | None = default(False),
        no_new_keyring: bool | None = default(False),
        pass_fds: int | None = default(0),  # NOTE: renaming intentinally
    ) -> "RunningContainer":
        args = (
            CLIArguments()
            / option("--bundle")(bundle)
            / option("--console-socket")(console_socket)
            / option("--pid-file")(pid_file)
            / flag("--no-pivot")(no_pivot)
            / flag("--no-new-keyring")(no_new_keyring)
            / option("--preserve-fds")(pass_fds)
        )

        if pass_fds is not None:
            self._run("create", *args.list, id, pass_fds=pass_fds)
        else:
            self._run("create", *args.list, id)

        return RunningContainer(self, id, io)

    def list(self) -> list[State]:
        result = self._run_unary(["list", "--format=json"])
        return json.decode(result, type=list[State])

    def state(self, id: str):
        result = self._run_unary(["state", id])
        return json.decode(result, type=State)

    @cached_property
    def features(self):
        result = self._run_unary(["features"])
        return json.decode(result, type=Features)


class RunningContainer:
    # TODO: Do we need to support IO=None?
    def __init__(self, runtime: Runc, id: str, io: IO | None = None) -> None:
        self._runtime = runtime
        self.id = id
        self.io = io

    def start(self) -> None:
        self._runtime._run_unary("start", self.id)

    def pause(self) -> None:
        self._runtime._run_unary("pause", self.id)

    def stop(self) -> None:
        self._runtime._run_unary("stop", self.id)

    def delete(self, force: bool | None = default(False)) -> None:
        args = CLIArguments() / flag("--force")(force)
        self._runtime._run_unary("delete", *args.list, self.id)
