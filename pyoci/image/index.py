from typing import TYPE_CHECKING, Literal

from pyoci.common import UNSET, Struct, Unset
from pyoci.image.descriptor import ContentDescriptor, ManifestDescriptor
from pyoci.image.const import MediaType, OciMediaType


class Index(Struct):
    manifests: list[ManifestDescriptor]

    if not TYPE_CHECKING:
        schemaVersion: Literal[2] = 2
        mediaType: Literal[OciMediaType.image_index] = OciMediaType.image_index

    artifactType: MediaType | Unset = UNSET
    subject: ContentDescriptor | Unset = UNSET
    annotations: dict[str, str] | Unset = UNSET
