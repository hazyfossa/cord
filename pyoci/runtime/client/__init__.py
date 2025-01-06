from typing import Literal

from msgspec import json
from pyoci.runtime.client.cli import (
    CLIArguments,
    default,
    flag,
    option,
)
from pyoci.runtime.client.executor import IO, AsyncRuntimeExecutor
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

        executor = AsyncRuntimeExecutor(path, self.__global_args__)
        self._run = executor.run
        self._run_unary = executor.run_unary

    async def create(
        self,
        id: str,
        bundle: str,
        io: IO = default(lambda: IO.current(), factory=True),
        console_socket: str | None = None,
        pid_file: str | None = None,
        no_pivot: bool | None = None,
        no_new_keyring: bool | None = None,
        preserve_fds: int | None = None,
    ) -> "RunningContainer":
        args = (
            CLIArguments()
            / option("--bundle")(bundle)
            / option("--console-socket")(console_socket)
            / option("--pid-file")(pid_file)
            / flag("--no-pivot")(no_pivot)
            / flag("--no-new-keyring")(no_new_keyring)
            / option("--preserve-fds")(preserve_fds)
        )

        await self._run_unary("create", *args.list, id)
        return RunningContainer(self, id, io)

    async def exec(
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
            / option("--console-socket")(console_socket)
            / option("--cwd")(cwd)
            / flag("--tty")(tty)
            / option("--user")(user)
            / option("--additional-gids")(additional_gids)
            / option("--process")(process)
            / flag("--detach")(detach)
            / option("--pid-file")(pid_file)
            / option("--process-label")(process_label)
            / option("--apparmor")(apparmor)
            / flag("--no-new-privs")(no_new_privs)
            / option("--cap")(cap)
            / option("--preserve-fds")(preserve_fds)
            / option("--cgroup")(cgroup)
            / flag("--ignore-paused")(ignore_paused)
        )

        await self._run_unary("exec", id, *args.list, *env_args)

    async def list(self) -> list[State]:
        result = await self._run_unary(["list", "--format=json"])
        return json.decode(result, type=list[State])

    async def state(self, id: str):
        result = await self._run_unary(["state", id])
        return json.decode(result, type=State)


class RunningContainer:
    def __init__(self, runtime: Runc, id: str, io: IO) -> None:
        self._runtime = runtime
        self.id = id

    async def start(self) -> None:
        await self._runtime._run_unary("start", self.id)

    async def pause(self) -> None:
        await self._runtime._run_unary("pause", self.id)

    async def stop(self) -> None:
        await self._runtime._run_unary("stop", self.id)

    async def delete(self, force: bool | None = default(False)) -> None:
        args = CLIArguments() / flag("--force")(force)
        await self._runtime._run_unary("delete", *args.list, self.id)
