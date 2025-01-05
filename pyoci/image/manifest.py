from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from pyoci.base_types import Annotations
from pyoci.common import Struct, const_field
from pyoci.image.descriptor import ContentDescriptor
from pyoci.image.const import MediaType


@const_field("schemaVersion", 2)
class ImageManifest(Struct):
    if not TYPE_CHECKING:
        schemaVersion: Literal[2]

    config: ContentDescriptor
    layers: Sequence[ContentDescriptor]

    mediaType: MediaType | None = None
    artifactType: MediaType | None = None
    subject: ContentDescriptor | None = None
    annotations: Annotations | None = None
