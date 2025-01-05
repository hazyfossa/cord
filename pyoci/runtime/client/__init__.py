from dataclasses import dataclass
from pathlib import Path
from subprocess import run, PIPE
from typing import Any, Literal

from msgspec import json

from pyoci.runtime.client import errors
from pyoci.runtime.client.cli import CLIArguments, default, flag, option
from pyoci.runtime.client.spec.features import Features
from pyoci.runtime.client.specific.runc import State


# Yes, this is much stricter than the OCI spec,
# but runc and crun will support that, and the basic spec is usually not enough
# TODO: Implement a pure-oci runtime interface, just in case
# TODO: cleanly support differences between runc and crun
class Runc:
    def __init__(
        self,
        path: str,
        handle_errors: bool = True,
        debug: bool | None = default(False),  # = False
        log: str | None = default("/dev/stderr"),  # = "/dev/stderr"
        log_format: str | None = default("text"),  # = "text"
        root: str | None = default("/run/user/1000//runc"),  # = "/run/user/1000//runc"
        systemd_cgroup: bool | None = default(False),  # = False
        rootless: bool | Literal["auto"] | None = default("auto"),  # = "auto"
    ):
        path = str(path)

        self.__global_args__ = (
            CLIArguments()
            / flag("--debug")
            / option("--log")
            / option("--log-format")
            / option("--root")
            / flag("--systemd-cgroup")
            / option("--rootless")(str(rootless).lower())
        ).list

        self._run = lambda *args: run(
            [path, *self.__global_args__, *args],
            capture_output=True,
        )

        if handle_errors:
            if log or log_format:
                raise ValueError(  # TODO: is this an appropriate Exception type?
                    "Setting log or log_format is not supported when using handle_errors"
                )

            log_format = "json"

            def run_with_error_handling(*args):
                result = self._run(*args)
                errors.handle(result)
                return result

            self._run = run_with_error_handling

    def create(
        self,
        id: str,
        bundle: str,
        console_socket: str | None = None,
        pid_file: str | None = None,
        no_pivot: bool | None = None,
        no_new_keyring: bool | None = None,
        preserve_fds: int | None = None,
    ):
        args = (
            CLIArguments()
            / option("--bundle")
            / option("--console-socket")
            / option("--pid-file")
            / flag("--no-pivot")
            / flag("--no-new-keyring")
            / option("--preserve-fds")
        )

        self._run("create", id, *args.list)

    def exec(
        self,
        id: str,
        console_socket: str | None = None,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        tty: bool | None = None,
        user: str | None = None,
        additional_gids: list[str] | None = None,
        process: str | None = None,
        detach: bool | None = None,
        pid_file: str | None = None,
        process_label: str | None = None,
        apparmor: str | None = None,
        no_new_privs: bool | None = None,
        cap: list[str] | None = None,
        preserve_fds: int | None = None,
        cgroup: str | None = None,
        ignore_paused: bool | None = None,
    ):
        env_args = (
            tuple(
                map(
                    lambda x: f"-e {'='.join(x)}",
                    env.items(),
                )
            )
            if env
            else None
        )

        args = (
            CLIArguments()
            / option("--console-socket")
            / option("--cwd")
            / flag("--tty")
            / option("--user")
            / option("--additional-gids")
            / option("--process")
            / flag("--detach")
            / option("--pid-file")
            / option("--process-label")
            / option("--apparmor")
            / flag("--no-new-privs")
            / option("--cap")
            / option("--preserve-fds")
            / option("--cgroup")
            / flag("--ignore-paused")
        )

        self._run("exec", id, *args.list, *env_args)

    def list(self) -> list[State]:
        result = self._run(["list", "--format json"])
        return json.decode(result.stdout, type=list[State])

    def state(self, id: str):
        result = self._run(["state", id])
        return json.decode(result.stdout, type=State)

    def start(self, id: str):
        self._run("start", id)

    def kill(self, id: str):
        self._run("stop", id)

    def delete(self, id: str, force: bool | None = None):
        args = CLIArguments() / flag("--force")
        self._run("delete", id, *args.list)


class StatefulRuntime: ...
