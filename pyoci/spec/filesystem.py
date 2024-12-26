from collections.abc import Sequence

from pyoci.spec.common import IDMapping, Struct

FilePath = str


class Root(Struct):
    path: FilePath
    readonly: bool | None = None


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
