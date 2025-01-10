from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal


from pyoci.base_types import Annotations, Data, Int64
from pyoci.common import UNSET, Struct, Unset
from pyoci.image.const import MediaType, OciMediaType
from pyoci.image.digest import Digest


class ContentDescriptor(Struct):
    """
    https://github.com/opencontainers/image-spec/blob/v1.1.0/descriptor.md
    """

    if not TYPE_CHECKING:
        mediaType: Literal[OciMediaType.content_descriptor] = (
            OciMediaType.content_descriptor
        )

    size: Int64  # in bytes
    digest: Digest

    urls: Sequence[str] | Unset = UNSET
    data: Data | Unset = UNSET
    artifactType: MediaType | Unset = UNSET
    annotations: Annotations | Unset = UNSET


class Platform(Struct):
    architecture: str
    os: str
    os_version: str | Unset = UNSET
    os_features: list[str] | Unset = UNSET
    variant: str | Unset = UNSET


class ManifestDescriptor(ContentDescriptor):
    platform: Platform | Unset = UNSET
