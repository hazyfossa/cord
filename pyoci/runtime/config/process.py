from collections.abc import Sequence
from typing import Annotated, Literal

from msgspec import Meta, field

from pyoci.common import Struct, Unset, UNSET
from pyoci.base_types import GID, UID, Int32, Uint32, Uint64

Umask = Uint32


class Rlimit(Struct):
    type: Annotated[str, Meta(pattern="^RLIMIT_[A-Z]+$")]
    hard: Uint64
    soft: Uint64


class IoPriority(Struct):
    class_: Literal[
        "IOPRIO_CLASS_RT",
        "IOPRIO_CLASS_BE",
        "IOPRIO_CLASS_IDLE",
    ] = field(name="class")

    priority: Int32 | Unset = UNSET


class ConsoleSize(Struct):
    height: Uint64
    width: Uint64


class ExecCPUAffinity(Struct):
    initial: Annotated[str, Meta(pattern="^[0-9, -]*$")] | Unset = UNSET
    final: Annotated[str, Meta(pattern="^[0-9, -]*$")] | Unset = UNSET


class User(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#user
    """

    username: str | Unset = UNSET
    uid: UID | Unset = UNSET
    gid: GID | Unset = UNSET

    umask: Umask | Unset = UNSET
    additionalGids: Sequence[GID] | Unset = UNSET


Env = list[str]

Capability = Annotated[
    str, Meta(pattern="^CAP_[A-Z_]+$")
]  # TODO does this need to be strict? Performance impact?


class Capabilities(Struct):
    bounding: Sequence[Capability] | Unset = UNSET
    permitted: Sequence[Capability] | Unset = UNSET
    effective: Sequence[Capability] | Unset = UNSET
    inheritable: Sequence[Capability] | Unset = UNSET
    ambient: Sequence[Capability] | Unset = UNSET


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
    nice: Int32 | Unset = UNSET
    priority: Int32 | Unset = UNSET
    flags: Sequence[SchedulerFlag] | Unset = UNSET
    runtime: Uint64 | Unset = UNSET
    deadline: Uint64 | Unset = UNSET
    period: Uint64 | Unset = UNSET


class Process(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#process
    """

    cwd: str
    args: Sequence[str] | Unset = UNSET
    env: Env | Unset = UNSET
    user: User | Unset = UNSET

    terminal: bool | Unset = UNSET
    consoleSize: ConsoleSize | Unset = UNSET

    capabilities: Capabilities | Unset = UNSET
    noNewPrivileges: bool | Unset = UNSET
    apparmorProfile: str | Unset = UNSET
    oomScoreAdj: int | Unset = UNSET
    selinuxLabel: str | Unset = UNSET

    ioPriority: IoPriority | Unset = UNSET
    scheduler: Scheduler | Unset = UNSET
    rlimits: Sequence[Rlimit] | Unset = UNSET
    execCPUAffinity: ExecCPUAffinity | Unset = UNSET

    commandLine: str | Unset = UNSET
