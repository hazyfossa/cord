from functools import cached_property
from io import BytesIO
from os import environ
from subprocess import PIPE, Popen
from typing import IO, Literal
from warnings import warn

from msgspec import json

from pyoci.runtime.client import errors
from pyoci.runtime.client.spec.features import Features
from pyoci.runtime.client.specific.runc import State
from pyoci.runtime.client.specific.runc.constraints import Constraints
from pyoci.runtime.client.utils import OpenIO, default

# warn(
#     "The oci runtime client is in alpha state, and isn't recommended for general usage."
# )

# TODO: filter out automatically
# Is this runc-specific?
if "NOTIFY_SOCKET" in environ:
    warn(
        "NOTIFY_SOCKET environment variable is set, and will be passed to the runtime, which may cause issues."
    )


# TODO: Implement a pure-oci runtime interface, just in case
# TODO: cleanly support differences between runc and crun
class Runc:
    def __init__(
        self,
        path: str = "runc",
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

        args = []
        if debug:
            args.append("--debug")
        if log:
            args.append(f"--log={log}")
        if log_format:
            args.append(f"--log-format={log_format}")
        if root:
            args.append(f"--root={root}")
        if systemd_cgroup:
            args.append("--systemd-cgroup")
        if rootless:
            args.append(f"--rootless={str(rootless).lower()}")

        self.__global_args__ = args

        def _run(
            *args,
            stdin: int | IO | None = None,
            stdout: int | IO | None = PIPE,
            wait: bool = True,
            **kwargs,
        ):
            process = Popen(
                [path, *self.__global_args__, *args],
                stdin=stdin,
                stdout=stdout,
                stderr=PIPE,  # TODO: errors without stderr
                process_group=0 if setpgid else None,
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
        args = []
        if bundle:
            args.append(f"--bundle={bundle}")
        if console_socket:
            args.append(f"--console-socket={console_socket}")
        if pid_file:
            args.append(f"--pid-file={pid_file}")
        if no_pivot:
            args.append("--no-pivot")
        if no_new_keyring:
            args.append("--no-new-keyring")
        if pass_fds:
            args.append(f"--preserve-fds={pass_fds}")

        proc = self._run(
            "create",
            *args,
            id,
            pass_fds=tuple(range(3, 3 + pass_fds)) if pass_fds is not None else (),
            stdin=PIPE,
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
        args = ["--force"] if force else []
        p = self._run("delete", *args, id)
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

    def update(self, id: str, new_constraints: Constraints):
        # TODO: use encode_into instead of BytesIO to save memory
        p = self._run(
            "update",
            "-r -",  # NOTE: this is required for runc to read from stdin
            id,
            stdin=BytesIO(json.encode(new_constraints)),
        )
        errors.handle(p)
