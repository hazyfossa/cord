from collections.abc import Sequence
from typing import Literal

from pyoci.spec.common import Struct
from pyoci.spec.int_types import Int32, Uint64

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
