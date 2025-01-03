from typing import TYPE_CHECKING
from pyoci.common import Struct, const_field
from pyoci.image.manifest import ContentDescriptor
from pyoci.image.descriptor import MediaType


@const_field("schemaVersion", 2)
class Index(Struct):
    if not TYPE_CHECKING:
        schemaVersion: Literal[2]

    manifests: list[ContentDescriptor]

    mediaType: MediaType | None = None
    artifactType: MediaType | None = None
    subject: ContentDescriptor | None = None
    annotations: dict[str, str] | None = None
