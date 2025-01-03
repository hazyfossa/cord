from collections.abc import Sequence
from typing import Annotated, Literal

from msgspec import Meta, field

from pyoci.common import Struct
from pyoci.base_types import GID, UID, Int32, Uint32, Uint64

Umask = Uint32


class Rlimit(Struct):
    hard: Uint64
    soft: Uint64
    type: Annotated[str, Meta(pattern="^RLIMIT_[A-Z]+$")]


class IoPriority(Struct):
    class_: Literal[
        "IOPRIO_CLASS_RT",
        "IOPRIO_CLASS_BE",
        "IOPRIO_CLASS_IDLE",
    ] = field(name="class")

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


Env = Sequence[str]

Capability = Annotated[
    str, Meta(pattern="^CAP_[A-Z_]+$")
]  # TODO does this need to be strict? Performance impact?


class Capabilities(Struct):
    bounding: Sequence[Capability] | None = None
    permitted: Sequence[Capability] | None = None
    effective: Sequence[Capability] | None = None
    inheritable: Sequence[Capability] | None = None
    ambient: Sequence[Capability] | None = None


SchedulerPolicy = Literal[
    "SCHED_OTHER",
    "SCHED_FIFO",
    "SCHED_RR",
    "SCHED_BATCH",
    "SCHED_ISO",
    "SCHED_IDLE",
    "SCHED_DEADLINE",
]

SchedulerFlag = Literal[
    "SCHED_FLAG_RESET_ON_FORK",
    "SCHED_FLAG_RECLAIM",
    "SCHED_FLAG_DL_OVERRUN",
    "SCHED_FLAG_KEEP_POLICY",
    "SCHED_FLAG_KEEP_PARAMS",
    "SCHED_FLAG_UTIL_CLAMP_MIN",
    "SCHED_FLAG_UTIL_CLAMP_MAX",
]


class Scheduler(Struct):
    policy: SchedulerPolicy
    nice: Int32 | None = None
    priority: Int32 | None = None
    flags: Sequence[SchedulerFlag] | None = None
    runtime: Uint64 | None = None
    deadline: Uint64 | None = None
    period: Uint64 | None = None


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
