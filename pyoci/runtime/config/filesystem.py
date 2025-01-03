from collections.abc import Sequence

from pyoci.common import Struct
from pyoci.base_types import Uint32

FilePath = str


class Root(Struct):
    path: FilePath
    readonly: bool | None = None


class IDMapping(Struct):
    containerID: Uint32
    hostID: Uint32
    size: Uint32


class Mount(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#mounts
    """

    destination: FilePath
    source: FilePath | None = None
    options: Sequence[str] | None = None
    type: str | None = None
    uidMappings: Sequence[IDMapping] | None = None
    gidMappings: Sequence[IDMapping] | None = None
