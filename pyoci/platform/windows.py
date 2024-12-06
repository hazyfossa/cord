from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pyoci.common import Struct
from pyoci.filesystem import FilePath
from pyoci.int_types import Uint16, Uint64


class Device(Struct):
    id: str
    idType: Literal["class"]


class Hyperv(Struct):
    utilityVMPath: str | None = None


class Network(Struct):
    endpointList: Sequence[str] | None = None
    allowUnqualifiedDNSQuery: bool | None = None
    DNSSearchList: Sequence[str] | None = None
    networkSharedContainerName: str | None = None
    networkNamespace: str | None = None


class Storage(Struct):
    iops: Uint64 | None = None
    bps: Uint64 | None = None
    sandboxSize: Uint64 | None = None


class Cpu(Struct):
    count: Uint64 | None = None
    shares: Uint16 | None = None
    maximum: Uint16 | None = None


class Memory(Struct):
    limit: Uint64 | None = None


class Resources(Struct):
    memory: Memory | None = None
    cpu: Cpu | None = None
    storage: Storage | None = None


class Windows(Struct):
    """
    Windows platform-specific configurations
    """

    layerFolders: Sequence[FilePath]
    devices: Sequence[Device] | None = None
    resources: Resources | None = None
    network: Network | None = None
    credentialSpec: Mapping[str, Any] | None = None
    servicing: bool | None = None
    ignoreFlushesDuringBoot: bool | None = None
    hyperv: Hyperv | None = None
