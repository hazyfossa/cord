from cord.base_types import UNSET, Int64, Uint16, Uint64, Unset
from cord.base_types import Struct


class Hugetlb(Struct):
    failcnt: Uint64
    usage: Uint64 | Unset = UNSET
    max: Uint64 | Unset = UNSET


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


class CPUSet(Struct):
    cpu_exclusive: Uint64

    mem_hardwall: Uint64
    mem_exclusive: Uint64
    memory_migrate: Uint64
    memory_spread_page: Uint64
    memory_spread_slab: Uint64
    memory_pressure: Uint64

    sched_load_balance: Uint64
    sched_relax_domain_level: Int64

    cpus: list[Uint16] | Unset = UNSET
    mems: list[Uint16] | Unset = UNSET


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


# NOTE: Intel RDT:


class L3CacheInfo(Struct):
    cbm_mask: str | Unset = UNSET
    min_cbm_bits: Uint64 | Unset = UNSET
    num_closids: Uint64 | Unset = UNSET


class MemBwInfo(Struct):
    bandwidth_gran: Uint64 | Unset = UNSET
    delay_linear: Uint64 | Unset = UNSET
    min_bandwidth: Uint64 | Unset = UNSET
    num_closids: Uint64 | Unset = UNSET


class MBMNumaNodeStats(Struct):
    mbm_total_bytes: Uint64 | Unset = UNSET
    mbm_local_bytes: Uint64 | Unset = UNSET


class CMTNumaNodeStats(Struct):
    llc_occupancy: Uint64 | Unset = UNSET


class IntelRdt(Struct):
    l3_cache_info: L3CacheInfo | Unset = UNSET
    l3_cache_schema_root: str | Unset = UNSET
    l3_cache_schema: str | Unset = UNSET

    mem_bw_info: MemBwInfo | Unset = UNSET
    mem_bw_schema_root: str | Unset = UNSET
    mem_bw_schema: str | Unset = UNSET

    mbm_stats: MBMNumaNodeStats | Unset = UNSET
    cmt_stats: CMTNumaNodeStats | Unset = UNSET


#


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
    cpuset: CPUSet
    memory: Memory
    pids: Pids
    blkio: Blkio
    hugetlb: dict[str, Hugetlb]
    intel_rdt: IntelRdt
    network_interfaces: list[NetworkInterface] | None = None


class Event(Struct):
    type: str
    id: str
    data: Stats | Unset = UNSET
