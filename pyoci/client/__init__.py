from dataclasses import dataclass
from pathlib import Path
from subprocess import run
from typing import Literal
from msgspec import json

from pyoci.client.cli import CLIArguments, flag, option
from pyoci.client.spec.state import State
from pyoci.client.spec.features import Features


@dataclass
class SystemdCgroup:
    slice: str
    prefix: str
    name: str

    def __str__(self):
        return ":".join([self.slice, self.prefix, self.name])


# Yes, this is much stricter than the OCI spec,
# but runc and crun will support that, and the basic spec is usually not enough
# TODO: Implement a pure-oci runtime interface, just in case
class Runtime:
    def __init__(
        self,
        path: str,
        debug: bool | None,  # = False
        log: str | None,  # = "/dev/stderr"
        log_format: str | None,  # = "text"
        root: str | None,  # = "/run/user/1000//runc"
        criu: str | None,  # = "criu"
        systemd_cgroup: SystemdCgroup | str | None,  # = False
        rootless: bool | Literal["auto"],  # = "auto"
    ):
        path = str(path)

        self.__global_args__ = (
            CLIArguments()
            / flag("--debug")(debug)
            / option("--log {}")(log)
            / option("--log-format {}")(log_format)
            / option("--root {}")(root)
            / option("--criu {}")(criu)
            / option("--systemd-cgroup {}")(systemd_cgroup)
            / option("--rootless")(str(rootless).lower())
        ).list

        self._run = lambda *args: run(
            [path, *self.__global_args__, *args],
        )

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
            / option("--bundle {}")(bundle)
            / option("--console-socket {}")(console_socket)
            / option("--pid-file {}")(pid_file)
            / option("--no-pivot")(no_pivot)
            / option("--no-new-keyring")(no_new_keyring)
            / option("--preserve-fds {}")(preserve_fds)
        ).list

        self._run("create", id, *args)

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
            / option("--console-socket {}")(console_socket)
            / option("--cwd {}")(cwd)
            / flag("--tty")(tty)
            / option("--user {}")(user)
            / option("--additional-gids {}")(additional_gids)
            / option("--process {}")(process)
            / flag("--detach")(detach)
            / option("--pid-file {}")(pid_file)
            / option("--process-label {}")(process_label)
            / option("--apparmor {}")(apparmor)
            / flag("--no-new-privs")(no_new_privs)
            / option("--cap {}")(cap)
            / option("--preserve-fds {}")(preserve_fds)
            / option("--cgroup {}")(cgroup)
            / flag("--ignore-paused")(ignore_paused)
        ).list

        self._run("exec", id, *args, *env_args)

    def state(self, id: str):
        result = self._run(["state", id])
        return json.decode(result.stdout, type=State)

    def start(self, id: str):
        self._run("start", id)

    def kill(self, id: str):
        self._run("stop", id)

    def delete(self, id: str, force: bool | None = None):
        args = CLIArguments() / flag("--force")(force)
        self._run("delete", id, *args.list)


class StatefulRuntime: ...
