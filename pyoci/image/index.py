from typing import TYPE_CHECKING
from pyoci.common import Struct, Unset, UNSET
from pyoci.image.descriptor import ContentDescriptor, ManifestDescriptor
from pyoci.image.descriptor import MediaType


class Index(Struct):
    manifests: list[ManifestDescriptor]

    if not TYPE_CHECKING:
        schemaVersion: Literal[2] = 2

    mediaType: MediaType | Unset = UNSET
    artifactType: MediaType | Unset = UNSET
    subject: ContentDescriptor | Unset = UNSET
    annotations: dict[str, str] | Unset = UNSET
