from collections.abc import Sequence

from pyoci.common import Struct, Unset, UNSET


class AnetItem(Struct):
    linkname: str | Unset = UNSET
    lowerLink: str | Unset = UNSET
    allowedAddress: str | Unset = UNSET
    configureAllowedAddress: str | Unset = UNSET
    defrouter: str | Unset = UNSET
    macAddress: str | Unset = UNSET
    linkProtection: str | Unset = UNSET


class CappedMemory(Struct):
    physical: str | Unset = UNSET
    swap: str | Unset = UNSET


class CappedCPU(Struct):
    ncpus: str | Unset = UNSET


class Solaris(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-solaris.md
    """

    milestone: str | Unset = UNSET
    limitpriv: str | Unset = UNSET
    maxShmMemory: str | Unset = UNSET
    cappedCPU: CappedCPU | Unset = UNSET
    cappedMemory: CappedMemory | Unset = UNSET
    anet: Sequence[AnetItem] | Unset = UNSET
