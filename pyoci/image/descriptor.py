from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from msgspec import field


from pyoci.base_types import Annotations, Data, Int64
from pyoci.common import UNSET, Struct, Unset
from pyoci.image.const import MediaType, OciMediaType
from pyoci.image.digest import Digest


class ContentDescriptor(Struct):
    """
    https://github.com/opencontainers/image-spec/blob/v1.1.0/descriptor.md
    """

    size: Int64  # in bytes
    digest: Digest

    urls: Sequence[str] | Unset = UNSET
    data: Data | Unset = UNSET
    artifactType: MediaType | Unset = UNSET
    annotations: Annotations | Unset = UNSET

    if not TYPE_CHECKING:
        # TODO: is this supposed to be static?
        mediaType: Literal[OciMediaType.content_descriptor] = (
            OciMediaType.content_descriptor
        )


class Platform(Struct):
    architecture: str
    os: str
    os_version: str | Unset = field(name="os.version", default=UNSET)
    # TODO: are there any well-known values for os features?
    os_features: list[str] | Unset = field(name="os.features", default=UNSET)
    variant: str | Unset = UNSET


# NOTE: Not part of the specification, used here for stronger typing
class ManifestDescriptor(ContentDescriptor):
    platform: Platform | Unset = UNSET
