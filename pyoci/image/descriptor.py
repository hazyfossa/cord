from collections.abc import Sequence
from typing import Annotated

from msgspec import Meta

from pyoci.base_types import Annotations, Data, Int64
from pyoci.common import Struct
from pyoci.image.digest import Digest
from pyoci.image.platform import Platform

MediaType = Annotated[
    str,
    Meta(
        pattern="^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}$"
    ),
]


class ContentDescriptor(Struct):
    """
    https://github.com/opencontainers/image-spec/blob/v1.1.0/descriptor.md
    """

    mediaType: MediaType
    size: Int64  # in bytes
    digest: Digest

    urls: Sequence[str] | None = None
    data: Data | None = None
    artifactType: MediaType | None = None
    annotations: Annotations | None = None


class ManifestDescriptor(ContentDescriptor):
    platform: Platform | None = None
