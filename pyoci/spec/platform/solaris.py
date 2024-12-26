from collections.abc import Sequence

from pyoci.spec.common import Struct


class AnetItem(Struct):
    linkname: str | None = None
    lowerLink: str | None = None
    allowedAddress: str | None = None
    configureAllowedAddress: str | None = None
    defrouter: str | None = None
    macAddress: str | None = None
    linkProtection: str | None = None


class CappedMemory(Struct):
    physical: str | None = None
    swap: str | None = None


class CappedCPU(Struct):
    ncpus: str | None = None


class Solaris(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-solaris.md
    """

    milestone: str | None = None
    limitpriv: str | None = None
    maxShmMemory: str | None = None
    cappedCPU: CappedCPU | None = None
    cappedMemory: CappedMemory | None = None
    anet: Sequence[AnetItem] | None = None
