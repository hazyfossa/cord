from datetime import datetime

from pyoci.common import UNSET, Struct, Unset
from pyoci.image.digest import DigestStr
from pyoci.image.platform import Platform

# TODO: allow specifying other templates if we dont merge this with the main structs
from pyoci.runtime.config.templates.default import (
    ContainerConfig,
    Process,
)


class RootFS(Struct):
    type: str
    diff_ids: list[DigestStr]


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

    def to_default_container_config(self) -> ContainerConfig:
        process = Process(
            cwd=self.WorkingDir or "/",  # TODO remove this non-spec default
            args=(self.Cmd or []) + (self.Entrypoint or []) or UNSET,
            env=self.Env,
        )

        raise NotImplementedError  # TODO
