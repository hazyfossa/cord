from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from cord.base_types import UNSET, Annotations, Struct, Unset
from cord.oci.image.descriptor import Descriptor, ManifestDescriptor
from cord.oci.image.well_known import MediaType, OciMediaType
from cord.utils.jsonstruct import JsonStruct


class Manifest(Struct, JsonStruct):
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


class Index(Struct, JsonStruct):
    # TODO: manifests can contain index descriptors. Do we consider index descriptors instances of ManifestDescriptor?
    # I.e. is "platform" valid on an index descriptor?
    manifests: list[ManifestDescriptor]

    artifactType: MediaType | Unset = UNSET
    subject: Descriptor | Unset = UNSET
    annotations: dict[str, str] | Unset = UNSET

    if not TYPE_CHECKING:
        schemaVersion: Literal[2] = 2
        mediaType: Literal[OciMediaType.image_index.value] = OciMediaType.image_index
