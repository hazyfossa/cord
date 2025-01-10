from functools import cached_property
from typing import Literal
from warnings import warn

from msgspec import json

from pyoci.runtime.client.cli import (
    CLIArguments,
    default,
    flag,
    option,
)
from pyoci.runtime.client.executor import RuntimeExecutor
from pyoci.runtime.client.io import OpenIO
from pyoci.runtime.client.spec.features import Features
from pyoci.runtime.client.specific.runc import State

warn(
    "The oci runtime client is in alpha state, and isn't recommended for general usage."
)


# TODO: Implement a pure-oci runtime interface, just in case
# TODO: cleanly support differences between runc and crun
class Runc:
    def __init__(
        self,
        path: str,
        handle_errors: bool = True,
        debug: bool | None = default(False),
        # TODO: can log be a pipe, so we can get logs even after container start?
        log: str | None = default("/dev/stderr"),
        log_format: Literal["text", "json"] | None = default("text"),
        root: str | None = default("/run/user/1000//runc"),
        systemd_cgroup: bool | None = default(False),
        rootless: bool | Literal["auto"] | None = default("auto"),
        setpgid: bool = False,
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

        executor = RuntimeExecutor(path, self.__global_args__, setpgid=setpgid)
        self._run = executor.run
        self._run_unary = executor.run_unary

    # TODO: separate the IO setup somehow
    def create(
        self,
        id: str,
        bundle: str,
        console_socket: str | None = None,
        pid_file: str | None = None,
        no_pivot: bool | None = default(False),
        no_new_keyring: bool | None = default(False),
        pass_fds: int | None = default(0),  # NOTE: renaming intentinally
    ) -> OpenIO:
        args = (
            CLIArguments()
            / option("--bundle")(bundle)
            / option("--console-socket")(console_socket)
            / option("--pid-file")(pid_file)
            / flag("--no-pivot")(no_pivot)
            / flag("--no-new-keyring")(no_new_keyring)
            / option("--preserve-fds")(pass_fds)
        )

        io = self._run(
            "create",
            *args.list,
            id,
            **(
                {"pass_fds": pass_fds} if pass_fds is not None else {}
            ),  # TODO: is this the right way to do this?
        )

        return io

    def start(self, id: str) -> None:
        self._run_unary("start", id)

    def pause(self, id: str) -> None:
        self._run_unary("pause", id)

    def stop(self, id: str) -> None:
        self._run_unary("stop", id)

    def delete(self, id: str, force: bool | None = default(False)) -> None:
        args = CLIArguments() / flag("--force")(force)
        self._run_unary("delete", *args.list, id)

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
