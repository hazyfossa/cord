from cord.base_types import UNSET, Unset
from cord.base_types import Struct

# NOTE: This is a (reduced) copy of cord.oci.runtime.platform.linux
# This needs to be done this way because the alternative (relocating these structs to platform.linux)
# ultimately requires oci schema definitions to depend on internal choices of runc.


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
