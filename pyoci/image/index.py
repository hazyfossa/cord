from typing import TYPE_CHECKING, Literal

from pyoci.common import UNSET, SimpleJsonMixin, Struct, Unset
from pyoci.image.descriptor import ContentDescriptor, ManifestDescriptor
from pyoci.image.const import MediaType, OciMediaType


class Index(Struct, SimpleJsonMixin):
    manifests: list[ManifestDescriptor]

    artifactType: MediaType | Unset = UNSET
    subject: ContentDescriptor | Unset = UNSET
    annotations: dict[str, str] | Unset = UNSET

    if not TYPE_CHECKING:
        schemaVersion: Literal[2] = 2
        mediaType: Literal[OciMediaType.image_index] = OciMediaType.image_index
