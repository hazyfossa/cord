from collections.abc import Sequence

from pyoci.base_types import Uint32
from pyoci.common import UNSET, Struct, Unset

FilePath = str


class Root(Struct):
    path: FilePath
    readonly: bool | Unset = UNSET


class IDMapping(Struct):
    containerID: Uint32
    hostID: Uint32
    size: Uint32


class Mount(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#mounts
    """

    destination: FilePath
    source: FilePath | Unset = UNSET
    options: Sequence[str] | Unset = UNSET
    type: str | Unset = UNSET
    uidMappings: Sequence[IDMapping] | Unset = UNSET
    gidMappings: Sequence[IDMapping] | Unset = UNSET
