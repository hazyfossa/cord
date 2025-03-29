from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from pyoci.base_types import Annotations
from pyoci.common import UNSET, SimpleJsonMixin, Struct, Unset
from pyoci.image.descriptor import Descriptor, ManifestDescriptor
from pyoci.image.well_known import MediaType, OciMediaType


class Manifest(Struct, SimpleJsonMixin):
    config: Descriptor
    layers: Sequence[Descriptor]

    artifactType: MediaType | Unset = UNSET
    subject: Descriptor | Unset = UNSET
    annotations: Annotations | Unset = UNSET

    if not TYPE_CHECKING:
        schemaVersion: Literal[2] = 2
        mediaType: Literal[OciMediaType.image_manifest.value] = (
            OciMediaType.image_manifest
        )


class Index(Struct, SimpleJsonMixin):
    # TODO: manifests can contain index descriptors. Do we consider index descriptors instances of ManifestDescriptor?
    # I.e. is "platform" valid on an index descriptor?
    manifests: list[ManifestDescriptor]

    artifactType: MediaType | Unset = UNSET
    subject: Descriptor | Unset = UNSET
    annotations: dict[str, str] | Unset = UNSET

    if not TYPE_CHECKING:
        schemaVersion: Literal[2] = 2
        mediaType: Literal[OciMediaType.image_index.value] = OciMediaType.image_index
