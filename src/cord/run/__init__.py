from datetime import timedelta
from functools import cached_property
from io import BytesIO
from os import environ
from pathlib import Path
from subprocess import PIPE
from typing import Literal, cast
from warnings import warn

from msgspec import json

from cord.run.spec.features import Features
from cord.run.specific.runc import State
from cord.run.specific.runc.constraints import Constraints
from cord.run.specific.runc.events import Event, Stats
from cord.run.utils import CLIWrapperBase, OpenIO
from cord.oci.runtime.process import Process


# TODO: filter out automatically
# Is this runc-specific?
if "NOTIFY_SOCKET" in environ:
    warn(
        "NOTIFY_SOCKET environment variable is set, and will be passed to the runtime, which may cause issues."
    )


# TODO: Implement a pure-oci runtime interface, just in case
# TODO: cleanly support differences between runc and crun
class Runc(CLIWrapperBase):
    def __init__(
        self,
        path: str | Path = "runc",
        debug: bool = False,
        root: str | None = None,
        systemd_cgroup: bool = False,
        rootless: bool | Literal["auto"] | None = None,
        setpgid: bool = False,
    ):
        # TODO: errors without stderr

        args = ["--log-format=json"]

        if debug:
            args.append("--debug")
        if root:
            args.append(f"--root={root}")
        if systemd_cgroup:
            args.append("--systemd-cgroup")
        if rootless:
            args.append(f"--rootless={str(rootless).lower()}")

        super().__init__(path, args, setpgid)

    # TODO: separate the IO setup somehow
    def create(
        self,
        id: str,
        bundle: str | Path,
        console_socket: str | None = None,
        pid_file: str | None = None,
        no_pivot: bool | None = False,
        no_new_keyring: bool | None = False,
        pass_fds: int | None = None,  # NOTE: renaming intentinally
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

        p = self._run_raw(
            "create",
            *args,
            id,
            pass_fds=tuple(range(3, 3 + pass_fds)) if pass_fds is not None else (),
            stdin=PIPE,
        )

        return OpenIO(p.stdin, p.stdout, p.stderr)  # type: ignore # TODO: IO

    def start(self, id: str) -> None:
        self._run("start", id)

    def exec(
        self,
        id: str,
        process: Process,
        console_socket: str | None = None,
        pid_file: str | None = None,
        detach: bool = False,
        ignore_paused: bool = False,
        pass_fds: int | None = None,  # NOTE: renaming intentinally
    ):
        # TODO: annotate detach with a proper type override
        args = []
        if console_socket:
            args.append(f"--console-socket={console_socket}")
        if pid_file:
            args.append(f"--pid-file={pid_file}")
        if detach:
            args.append("--detach")
        if ignore_paused:
            args.append("--ignore-paused")
        if pass_fds:
            args.append(f"--preserve-fds={pass_fds}")

        p = self._run_raw(
            "exec",
            *args,
            "-p -",
            id,
            stdin=BytesIO(
                json.encode(process)
            ),  # TODO: we cannot take stdin here, as it'll be passed to the executed process
            pass_fds=tuple(range(3, 3 + pass_fds)) if pass_fds is not None else (),
        )

        if not detach:
            return OpenIO(p.stdin, p.stdout, p.stderr)  # type: ignore # TODO: IO

    def pause(self, id: str) -> None:
        self._run("pause", id)

    def resume(self, id: str) -> None:
        self._run("resume", id)

    def kill(
        self,
        id: str,
        signal: str | None = "SIGTERM",
        all: bool = False,
    ) -> None:
        args = ["--all"] if all else []
        self._run("kill", *args, id, signal)

    def delete(self, id: str, force: bool = False) -> None:
        args = ["--force"] if force else []
        self._run("delete", *args, id)

    def list(self) -> list[State]:
        stdout = self._run("list", "--format=json")
        return json.decode(stdout.read(), type=list[State])

    def state(self, id: str):
        stdout = self._run("state", id)
        return json.decode(stdout.read(), type=State)

    def stats(self, id: str):
        stdout = self._run("events", "--stats", id)
        return cast(Stats, json.decode(stdout.read(), type=Event).data)

    # def events(self, id: str, update_interval: timedelta | None): ... # TODO

    @cached_property
    def features(self):
        stdout = self._run("features")

        return json.decode(stdout.read(), type=Features)

    def update(self, id: str, new_constraints: Constraints):
        # TODO: use encode_into instead of BytesIO to save memory
        self._run(
            "update",
            "-r -",
            id,
            stdin=BytesIO(json.encode(new_constraints)),
        )
