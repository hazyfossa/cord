from pyoci.base_types import Uint64
from pyoci.common import Struct, Unset, UNSET


class BlkioEntry(Struct):
    major: Uint64 | Unset = UNSET
    minor: Uint64 | Unset = UNSET
    op: str | Unset = UNSET
    value: Uint64 | Unset = UNSET


class Blkio(Struct):
    ioServiceBytesRecursive: list[BlkioEntry] | Unset = UNSET
    ioServicedRecursive: list[BlkioEntry] | Unset = UNSET
    ioQueuedRecursive: list[BlkioEntry] | Unset = UNSET
    ioServiceTimeRecursive: list[BlkioEntry] | Unset = UNSET
    ioWaitTimeRecursive: list[BlkioEntry] | Unset = UNSET
    ioMergedRecursive: list[BlkioEntry] | Unset = UNSET
    ioTimeRecursive: list[BlkioEntry] | Unset = UNSET
    sectorsRecursive: list[BlkioEntry] | Unset = UNSET


class Pids(Struct):
    current: Uint64 | Unset = UNSET
    limit: Uint64 | Unset = UNSET


class Throttling(Struct):
    periods: Uint64 | Unset = UNSET
    throttledPeriods: Uint64 | Unset = UNSET
    throttledTime: Uint64 | Unset = UNSET


class CpuUsage(Struct):
    kernel: Uint64
    user: Uint64
    total: Uint64 | Unset = UNSET
    percpu: list[Uint64] | Unset = UNSET


class Cpu(Struct):
    usage: CpuUsage | Unset = UNSET
    throttling: Throttling | Unset = UNSET


class MemoryEntry(Struct):
    failcnt: Uint64
    limit: Uint64
    usage: Uint64 | Unset = UNSET
    max: Uint64 | Unset = UNSET


class Memory(Struct):
    cache: Uint64 | Unset = UNSET
    usage: MemoryEntry | Unset = UNSET
    swap: MemoryEntry | Unset = UNSET
    kernel: MemoryEntry | Unset = UNSET
    kernelTCP: MemoryEntry | Unset = UNSET
    raw: dict[str, Uint64] | Unset = UNSET


class Hugetlb(Struct):
    failcnt: Uint64
    usage: Uint64 | Unset = UNSET
    max: Uint64 | Unset = UNSET


class NetworkInterface(Struct):
    name: str

    rx_bytes: Uint64
    rx_packets: Uint64
    rx_errors: Uint64
    rx_dropped: Uint64
    tx_bytes: Uint64
    tx_packets: Uint64
    tx_errors: Uint64
    tx_dropped: Uint64


class Stats(Struct):
    cpu: Cpu
    memory: Memory
    pids: Pids
    blkio: Blkio
    hugetlb: dict[str, Hugetlb]
    network_interfaces: list[NetworkInterface]


class Event(Struct):
    type: str
    id: str
    data: Stats | Unset = UNSET
