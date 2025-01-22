from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from pyoci.base_types import Annotations
from pyoci.common import UNSET, SimpleJsonMixin, Struct, Unset
from pyoci.image.const import MediaType, OciMediaType
from pyoci.image.descriptor import ContentDescriptor


class ImageManifest(Struct, SimpleJsonMixin):
    config: ContentDescriptor
    layers: Sequence[ContentDescriptor]

    artifactType: MediaType | Unset = UNSET
    subject: ContentDescriptor | Unset = UNSET
    annotations: Annotations | Unset = UNSET

    if not TYPE_CHECKING:
        schemaVersion: Literal[2] = 2
        mediaType: Literal[OciMediaType.image_manifest] = OciMediaType.image_manifest
