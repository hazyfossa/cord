from datetime import datetime

from msgspec import Struct
from pyoci.common import UNSET, Unset

from pyoci.image.digest import Digest
from pyoci.image.platform import Platform
from pyoci.runtime.config import Container as Config
from pyoci.runtime.config.process import Process


class RootFS(Struct):
    type: str
    diff_ids: list[Digest]


class History(Struct):
    created: datetime | Unset = UNSET
    created_by: str | Unset = UNSET
    author: str | Unset = UNSET
    comment: str | Unset = UNSET
    empty_layer: bool | Unset = UNSET


class Image(Struct):
    rootfs: RootFS
    platform: Platform

    created: datetime | Unset = UNSET
    author: str | Unset = UNSET
    config: "ImageConfig | None" = None
    history: list[History] | Unset = UNSET


class ImageConfig(
    Struct
):  # TODO: conside renaming the python reflection's fields for consistency
    """
    https://github.com/opencontainers/image-spec/blob/v1.1.0/config.md
    """

    User: str | Unset = UNSET
    ExposedPorts: dict[str, None] | Unset = UNSET
    Env: list[str] | Unset = UNSET
    Entrypoint: list[str] | Unset = UNSET
    Cmd: list[str] | Unset = UNSET
    Volumes: dict[str, None] | Unset = UNSET
    WorkingDir: str | Unset = UNSET
    Labels: dict[str, str] | Unset = UNSET
    StopSignal: str | Unset = UNSET

    def to_bundle(self) -> Config:
        process = Process(
            cwd=self.WorkingDir or "/",  # TODO remove this non-spec default
            args=(self.Cmd or []) + (self.Entrypoint or []) or UNSET,
            env=self.Env,
        )
