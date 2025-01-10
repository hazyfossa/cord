from enum import StrEnum
from msgspec import field
from pyoci.common import Struct, Unset, UNSET

_type_oci = "application/vnd.oci"


# fmt: off
class MediaType(StrEnum):
    content_descriptor = "application/vnd.oci.image.descriptor.v1+json"
    layout =             "application/vnd.oci.image.layout.v1+json"
    image_manifest =     "application/vnd.oci.image.manifest.v1+json"
    image_index =        "application/vnd.oci.image.index.v1+json"
    image_config =       "application/vnd.oci.image.config.v1+json"
    empty =              "application/vnd.oci.image.layer.v1.empty"

    layer =              "application/vnd.oci.image.layer.v1.tar"
    layer_gzip =         "application/vnd.oci.image.layer.v1.tar+gzip"
    layer_zstd =         "application/vnd.oci.image.layer.v1.tar+zstd"
# fmt: on


def annotation(name: str) -> Unset:
    return field(name=f"org.opencontainers.image.annotation.{name}", default=UNSET)


class ImageAnnotation(Struct):
    created: str | Unset = annotation("created")
    authors: str | Unset = annotation("authors")
    url: str | Unset = annotation("url")
    documentation: str | Unset = annotation("documentation")
    source: str | Unset = annotation("source")
    version: str | Unset = annotation("version")
    revision: str | Unset = annotation("revision")
    vendor: str | Unset = annotation("vendor")
    licenses: str | Unset = annotation("licenses")
    ref_name: str | Unset = annotation("ref.name")
    title: str | Unset = annotation("title")
    description: str | Unset = annotation("description")
    base_image_digest: str | Unset = annotation("base.digest")
    base_image_name: str | Unset = annotation("base.name")
