from pyoci.common import Struct, Unset, UNSET

# NOTE: This is a (reduced) copy of pyoci.runtime.config.platform.linux
# This needs to be done this way because the alternative (relocating these structs to platform.linux)
# ultimately requires pyoci schema to depend on internal choices of runc.


class Memory(Struct):
    limit: int
    reservation: int | Unset = UNSET
    swap: int | Unset = UNSET


class CPU(Struct):
    shares: int | Unset = UNSET
    quota: int | Unset = UNSET
    period: int | Unset = UNSET
    realtimeRuntime: int | Unset = UNSET
    realtimePeriod: int | Unset = UNSET
    cpus: str | Unset = UNSET
    mems: str | Unset = UNSET


class BlockIO(Struct):
    weight: int | Unset = UNSET


class Constraints(Struct):
    memory: Memory | Unset = UNSET
    cpu: CPU | Unset = UNSET
    blockIO: BlockIO | Unset = UNSET
