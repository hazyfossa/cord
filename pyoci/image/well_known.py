from enum import StrEnum
from typing import Annotated

from msgspec import Meta, field

from pyoci.common import UNSET, Struct, Unset

MediaType = Annotated[
    str,
    Meta(
        pattern="^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}$"
    ),
]


# fmt: off

class OciMediaType(StrEnum):
    content_descriptor = "application/vnd.oci.image.descriptor.v1+json"
    layout =             "application/vnd.oci.image.layout.v1+json"
    image_manifest =     "application/vnd.oci.image.manifest.v1+json"
    image_index =        "application/vnd.oci.image.index.v1+json"
    image_config =       "application/vnd.oci.image.config.v1+json"
    empty =              "application/vnd.oci.image.layer.v1.empty"

    layer =              "application/vnd.oci.image.layer.v1.tar"
    layer_gzip =         "application/vnd.oci.image.layer.v1.tar+gzip"
    layer_zstd =         "application/vnd.oci.image.layer.v1.tar+zstd"


class ImageAnnotation(StrEnum):
    created =           "org.opencontainers.image.annotation.created"
    authors =           "org.opencontainers.image.annotation.authors"
    url =               "org.opencontainers.image.annotation.url"
    documentation =     "org.opencontainers.image.annotation.documentation"
    source =            "org.opencontainers.image.annotation.source"
    version =           "org.opencontainers.image.annotation.version"
    revision =          "org.opencontainers.image.annotation.revision"
    vendor =            "org.opencontainers.image.annotation.vendor"
    licenses =          "org.opencontainers.image.annotation.licenses"
    ref_name =          "org.opencontainers.image.annotation.ref.name"
    _title =             "org.opencontainers.image.annotation.title"
    description =       "org.opencontainers.image.annotation.description"
    base_image_digest = "org.opencontainers.image.annotation.base.digest"
    base_image_name =   "org.opencontainers.image.annotation.base.name"

# fmt: on


def _runtime_annotation(key: str) -> Unset:
    return field(name=f"org.opencontainers.image.{key}", default=UNSET)


# TODO
class RuntimeConfigAnnotations(Struct):
    os: str | Unset = _runtime_annotation("os")
    architecture: str | Unset = _runtime_annotation("architecture")
