from datetime import datetime

from pyoci.common import Struct
from pyoci.image.digest import Digest
from pyoci.image.platform import Platform


class ImageConfig(
    Struct
):  # TODO: conside renaming the python reflection's fields for consistency
    User: str | None = None
    ExposedPorts: dict[str, None] | None = None
    Env: list[str] | None = None
    Entrypoint: list[str] | None = None
    Cmd: list[str] | None = None
    Volumes: dict[str, None] | None = None
    WorkingDir: str | None = None
    Labels: dict[str, str] | None = None
    StopSignal: str | None = None


class RootFS(Struct):
    type: str
    diff_ids: list[Digest]


class History(Struct):
    created: datetime | None = None
    created_by: str | None = None
    author: str | None = None
    comment: str | None = None
    empty_layer: bool | None = None


class Image(Struct):
    rootfs: RootFS
    platform: Platform

    created: datetime | None = None
    author: str | None = None
    config: ImageConfig | None = None
    history: list[History] | None = None
