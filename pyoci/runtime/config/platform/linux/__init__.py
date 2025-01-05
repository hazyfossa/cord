from collections.abc import Mapping, Sequence
from typing import Annotated, Literal

from msgspec import Meta

from pyoci.base_types import Int64, Uint32, Uint64
from pyoci.common import Struct, Unset, UNSET
from pyoci.runtime.config.filesystem import FilePath, IDMapping
from pyoci.runtime.config.platform.linux.devices import BlockIO, Device, DeviceCgroup
from pyoci.runtime.config.platform.linux.seccomp import Seccomp


class TimeOffsets(Struct):
    secs: Int64 | Unset = UNSET
    nanosecs: Uint32 | Unset = UNSET


class PlatformTimeOffsets(Struct):
    boottime: TimeOffsets | Unset = UNSET
    monotonic: TimeOffsets | Unset = UNSET


class IntelRdt(Struct):
    closID: str | Unset = UNSET
    l3CacheSchema: str | Unset = UNSET
    memBwSchema: Annotated[str, Meta(pattern="^MB:[^\\n]*$")] | Unset = UNSET
    enableCMT: bool | Unset = UNSET
    enableMBM: bool | Unset = UNSET


class NetworkInterfacePriority(Struct):
    name: str
    priority: Uint32


class Network(Struct):
    classID: Uint32 | Unset = UNSET
    priorities: Sequence[NetworkInterfacePriority] | Unset = UNSET


class Memory(Struct):
    kernel: Int64 | Unset = UNSET
    kernelTCP: Int64 | Unset = UNSET
    limit: Int64 | Unset = UNSET
    reservation: Int64 | Unset = UNSET
    swap: Int64 | Unset = UNSET
    swappiness: Uint64 | Unset = UNSET
    disableOOMKiller: bool | Unset = UNSET
    useHierarchy: bool | Unset = UNSET
    checkBeforeUpdate: bool | Unset = UNSET


class HugepageLimit(Struct):
    pageSize: Annotated[str, Meta(pattern="^[1-9][0-9]*[KMG]B$")]
    limit: Uint64


class Cpu(Struct):
    cpus: str | Unset = UNSET
    mems: str | Unset = UNSET
    period: Uint64 | Unset = UNSET
    quota: Int64 | Unset = UNSET
    burst: Uint64 | Unset = UNSET
    realtimePeriod: Uint64 | Unset = UNSET
    realtimeRuntime: Int64 | Unset = UNSET
    shares: Uint64 | Unset = UNSET
    idle: Int64 | Unset = UNSET


class Rdma(Struct):
    hcaHandles: Uint32 | Unset = UNSET
    hcaObjects: Uint32 | Unset = UNSET


class Pids(Struct):
    limit: Int64


class Resources(Struct):
    unified: Mapping[str, str] | Unset = UNSET
    devices: Sequence[DeviceCgroup] | Unset = UNSET
    pids: Pids | Unset = UNSET
    blockIO: BlockIO | Unset = UNSET
    cpu: Cpu | Unset = UNSET
    hugepageLimits: Sequence[HugepageLimit] | Unset = UNSET
    memory: Memory | Unset = UNSET
    network: Network | Unset = UNSET
    rdma: Mapping[str, Rdma] | Unset = UNSET


NamespaceType = Literal[
    "mount", "pid", "network", "uts", "ipc", "user", "cgroup", "time"
]


class Namespace(Struct):
    type: NamespaceType
    path: FilePath | Unset = UNSET


RootfsPropagation = Literal["private", "shared", "slave", "unbindable"]


class Personality(Struct):
    domain: Literal["LINUX", "LINUX32"] | Unset = UNSET
    flags: Sequence[str] | Unset = UNSET


class Linux(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md
    """

    devices: Sequence[Device] | Unset = UNSET
    uidMappings: Sequence[IDMapping] | Unset = UNSET
    gidMappings: Sequence[IDMapping] | Unset = UNSET
    namespaces: Sequence[Namespace] | Unset = UNSET
    resources: Resources | Unset = UNSET
    cgroupsPath: str | Unset = UNSET
    rootfsPropagation: RootfsPropagation | Unset = UNSET
    seccomp: Seccomp | Unset = UNSET
    sysctl: Mapping[str, str] | Unset = UNSET
    maskedPaths: Sequence[str] | Unset = UNSET
    readonlyPaths: Sequence[str] | Unset = UNSET
    mountLabel: str | Unset = UNSET
    intelRdt: IntelRdt | Unset = UNSET
    personality: Personality | Unset = UNSET
    timeOffsets: PlatformTimeOffsets | Unset = UNSET
