from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pyoci.common import Struct, Unset, UNSET
from pyoci.runtime.config.filesystem import FilePath
from pyoci.base_types import Uint16, Uint64


class Device(Struct):
    id: str
    idType: Literal["class"]


class Hyperv(Struct):
    utilityVMPath: str | Unset = UNSET


class Network(Struct):
    endpointList: Sequence[str] | Unset = UNSET
    allowUnqualifiedDNSQuery: bool | Unset = UNSET
    DNSSearchList: Sequence[str] | Unset = UNSET
    networkSharedContainerName: str | Unset = UNSET
    networkNamespace: str | Unset = UNSET


class Storage(Struct):
    iops: Uint64 | Unset = UNSET
    bps: Uint64 | Unset = UNSET
    sandboxSize: Uint64 | Unset = UNSET


class Cpu(Struct):
    count: Uint64 | Unset = UNSET
    shares: Uint16 | Unset = UNSET
    maximum: Uint16 | Unset = UNSET


class Memory(Struct):
    limit: Uint64 | Unset = UNSET


class Resources(Struct):
    memory: Memory | Unset = UNSET
    cpu: Cpu | Unset = UNSET
    storage: Storage | Unset = UNSET


class Windows(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-windows.md
    """

    layerFolders: Sequence[FilePath]
    devices: Sequence[Device] | Unset = UNSET
    resources: Resources | Unset = UNSET
    network: Network | Unset = UNSET
    credentialSpec: Mapping[str, Any] | Unset = UNSET
    servicing: bool | Unset = UNSET
    ignoreFlushesDuringBoot: bool | Unset = UNSET
    hyperv: Hyperv | Unset = UNSET
