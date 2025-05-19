from typing import dataclass_transform, Protocol
from cord.base_types import UNSET, Struct, Unset


# TODO: replace with automatic binding once clwrap v2 is ready
@dataclass_transform()
class CliArgs(Protocol):
    def to_cli(self) -> list[str]: ...


class ContainerRef(Struct):
    id: str
    bundle: str | Unset = UNSET

    def to_cli(self) -> list[str]:
        args = [self.id]
        if self.bundle:
            args.append(f"--bundle={self.bundle}")
        return args


class ProcessInit(Struct):
    console_socket: str | Unset = UNSET
    pid_file: str | Unset = UNSET
    no_pivot: bool | Unset = UNSET
    no_new_keyring: bool | Unset = UNSET
    pass_fds: int | Unset = UNSET

    def to_cli(self) -> list[str]:
        args = []
        if self.console_socket:
            args.append(f"--console-socket={self.console_socket}")
        if self.pid_file:
            args.append(f"--pid-file={self.pid_file}")
        if self.no_pivot:
            args.append("--no-pivot")
        if self.no_new_keyring:
            args.append("--no-new-keyring")
        if self.pass_fds:
            args.append(f"--preserve-fds={self.pass_fds}")
        return args
