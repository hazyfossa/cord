from collections.abc import Sequence
from typing import Literal

from pyoci.base_types import Uint32, Uint64
from pyoci.common import Struct, Unset, UNSET

SeccompOperators = Literal[
    "SCMP_CMP_NE",
    "SCMP_CMP_LT",
    "SCMP_CMP_LE",
    "SCMP_CMP_EQ",
    "SCMP_CMP_GE",
    "SCMP_CMP_GT",
    "SCMP_CMP_MASKED_EQ",
]

SeccompFlag = Literal[
    "SECCOMP_FILTER_FLAG_TSYNC",
    "SECCOMP_FILTER_FLAG_LOG",
    "SECCOMP_FILTER_FLAG_SPEC_ALLOW",
    "SECCOMP_FILTER_FLAG_WAIT_KILLABLE_RECV",
]

SeccompAction = Literal[
    "SCMP_ACT_KILL",
    "SCMP_ACT_KILL_PROCESS",
    "SCMP_ACT_KILL_THREAD",
    "SCMP_ACT_TRAP",
    "SCMP_ACT_ERRNO",
    "SCMP_ACT_TRACE",
    "SCMP_ACT_ALLOW",
    "SCMP_ACT_LOG",
    "SCMP_ACT_NOTIFY",
]

SeccompArch = Literal[
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X32",
    "SCMP_ARCH_ARM",
    "SCMP_ARCH_AARCH64",
    "SCMP_ARCH_MIPS",
    "SCMP_ARCH_MIPS64",
    "SCMP_ARCH_MIPS64N32",
    "SCMP_ARCH_MIPSEL",
    "SCMP_ARCH_MIPSEL64",
    "SCMP_ARCH_MIPSEL64N32",
    "SCMP_ARCH_PPC",
    "SCMP_ARCH_PPC64",
    "SCMP_ARCH_PPC64LE",
    "SCMP_ARCH_S390",
    "SCMP_ARCH_S390X",
    "SCMP_ARCH_PARISC",
    "SCMP_ARCH_PARISC64",
    "SCMP_ARCH_RISCV64",
]


class SyscallArg(Struct):
    index: Uint32
    value: Uint64
    op: SeccompOperators
    valueTwo: Uint64 | Unset = UNSET


class Syscall(Struct):
    names: Sequence[str]
    action: SeccompAction
    errnoRet: Uint32 | Unset = UNSET
    args: Sequence[SyscallArg] | Unset = UNSET


class Seccomp(Struct):
    defaultAction: SeccompAction
    defaultErrnoRet: Uint32 | Unset = UNSET
    flags: Sequence[SeccompFlag] | Unset = UNSET
    listenerPath: str | Unset = UNSET
    listenerMetadata: str | Unset = UNSET
    architectures: Sequence[SeccompArch] | Unset = UNSET
    syscalls: Sequence[Syscall] | Unset = UNSET


class SeccompFeature(Struct):
    enabled: bool | Unset = UNSET
    actions: Sequence[SeccompAction] | Unset = UNSET
    operators: Sequence[SeccompOperators] | Unset = UNSET
    archs: Sequence[SeccompArch] | Unset = UNSET
    knownFlags: Sequence[SeccompFlag] | Unset = UNSET
    supportedFlags: Sequence[SeccompFlag] | Unset = UNSET
