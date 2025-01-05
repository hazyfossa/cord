from pyoci.base_types import Uint64
from pyoci.common import Struct


class BlkioEntry(Struct):
    major: Uint64 | None = None
    minor: Uint64 | None = None
    op: str | None = None
    value: Uint64 | None = None


class Blkio(Struct):
    ioServiceBytesRecursive: list[BlkioEntry] | None = None
    ioServicedRecursive: list[BlkioEntry] | None = None
    ioQueuedRecursive: list[BlkioEntry] | None = None
    ioServiceTimeRecursive: list[BlkioEntry] | None = None
    ioWaitTimeRecursive: list[BlkioEntry] | None = None
    ioMergedRecursive: list[BlkioEntry] | None = None
    ioTimeRecursive: list[BlkioEntry] | None = None
    sectorsRecursive: list[BlkioEntry] | None = None


class Pids(Struct):
    current: Uint64 | None = None
    limit: Uint64 | None = None


class Throttling(Struct):
    periods: Uint64 | None = None
    throttledPeriods: Uint64 | None = None
    throttledTime: Uint64 | None = None


class CpuUsage(Struct):
    kernel: Uint64
    user: Uint64
    total: Uint64 | None = None
    percpu: list[Uint64] | None = None


class Cpu(Struct):
    usage: CpuUsage | None = None
    throttling: Throttling | None = None


class MemoryEntry(Struct):
    failcnt: Uint64
    limit: Uint64
    usage: Uint64 | None = None
    max: Uint64 | None = None


class Memory(Struct):
    cache: Uint64 | None = None
    usage: MemoryEntry | None = None
    swap: MemoryEntry | None = None
    kernel: MemoryEntry | None = None
    kernelTCP: MemoryEntry | None = None
    raw: dict[str, Uint64] | None = None


class Hugetlb(Struct):
    failcnt: Uint64
    usage: Uint64 | None = None
    max: Uint64 | None = None


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
    data: Stats | None = None
