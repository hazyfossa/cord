from functools import cached_property
from subprocess import PIPE, Popen
from typing import Literal
from warnings import warn

from msgspec import json

from pyoci.runtime.client import errors
from pyoci.runtime.client.cli import (
    CLIArguments,
    default,
    flag,
    option,
)
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
        # TODO: errors without stderr
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
                raise ValueError(
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

        def _run(
            *args,
            input: bool = False,
            output: bool = True,
            wait: bool = True,
            **kwargs,
        ):
            process = Popen(
                [path, *self.__global_args__, *args],
                stdin=PIPE if input else None,
                stdout=PIPE if output else None,
                stderr=PIPE,  # TODO: errors without stderr
                **kwargs,
            )

            if wait:
                process.wait()

            return process

        self._run = _run

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

        proc = self._run(
            "create",
            *args.list,
            id,
            pass_fds=tuple(range(3, 3 + pass_fds)) if pass_fds is not None else (),
        )

        return OpenIO(proc.stdin, proc.stdout, proc.stderr)  # type: ignore # TODO: IO

    def start(self, id: str) -> None:
        self._run("start", id)

    def pause(self, id: str) -> None:
        p = self._run("pause", id)
        errors.handle(p)

    def stop(self, id: str) -> None:
        p = self._run("stop", id)
        errors.handle(p)

    def delete(self, id: str, force: bool | None = default(False)) -> None:
        args = CLIArguments() / flag("--force")(force)
        p = self._run("delete", *args.list, id)
        errors.handle(p)

    def list(self) -> list[State]:
        p = self._run("list", "--format=json")
        errors.handle(p)
        return json.decode(p.stdout.read(), type=list[State])  # type: ignore # TODO: IO

    def state(self, id: str):
        p = self._run("state", id)
        errors.handle(p)
        return json.decode(p.stdout.read(), type=State)  # type: ignore # TODO: IO

    @cached_property
    def features(self):
        p = self._run("features")
        errors.handle(p)
        return json.decode(p.stdout.read(), type=Features)  # type: ignore # TODO: IO
