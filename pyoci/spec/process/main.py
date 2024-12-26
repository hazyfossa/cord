from collections.abc import Sequence
from typing import Annotated, Literal

from msgspec import Meta, field

from pyoci.spec.common import GID, UID, Env, Struct
from pyoci.spec.int_types import Int32, Uint32, Uint64
from pyoci.spec.process.capabilities import Capabilities
from pyoci.spec.process.scheduler import Scheduler

Umask = Uint32


class Rlimit(Struct):
    hard: Uint64
    soft: Uint64
    type: Annotated[str, Meta(pattern="^RLIMIT_[A-Z]+$")]


class IoPriority(Struct):
    class_: Literal["IOPRIO_CLASS_RT", "IOPRIO_CLASS_BE", "IOPRIO_CLASS_IDLE"] = field(name="class")
    priority: Int32 | None = None


class ConsoleSize(Struct):
    height: Uint64
    width: Uint64


class ExecCPUAffinity(Struct):
    initial: Annotated[str, Meta(pattern="^[0-9, -]*$")] | None = None
    final: Annotated[str, Meta(pattern="^[0-9, -]*$")] | None = None


class User(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#user
    """
    uid: UID | None = None
    gid: GID | None = None
    umask: Umask | None = None
    additionalGids: Sequence[GID] | None = None
    username: str | None = None


class Process(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#process
    """
    cwd: str
    args: Sequence[str] | None = None
    commandLine: str | None = None
    consoleSize: ConsoleSize | None = None
    env: Env | None = None
    terminal: bool | None = None
    user: User | None = None
    capabilities: Capabilities | None = None
    apparmorProfile: str | None = None
    oomScoreAdj: int | None = None
    selinuxLabel: str | None = None
    ioPriority: IoPriority | None = None
    noNewPrivileges: bool | None = None
    scheduler: Scheduler | None = None
    rlimits: Sequence[Rlimit] | None = None
    execCPUAffinity: ExecCPUAffinity | None = None
