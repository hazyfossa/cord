from enum import StrEnum
from msgspec import field
from pyoci.common import Struct

_type_oci = "application/vnd.oci"


class MediaType(StrEnum):
    content_descriptor = f"{_type_oci}.image.descriptor.v1+json"
    layout = f"{_type_oci}.layout.header.v1+json"
    image_manifest = f"{_type_oci}.image.manifest.v1+json"
    image_index = f"{_type_oci}.image.index.v1+json"
    image_config = f"{_type_oci}.image.config.v1+json"
    empty = f"{_type_oci}.empty.v1+json"

    layer = f"{_type_oci}.image.layer.v1.tar"
    layer_gzip = f"{_type_oci}.image.layer.v1.tar+gzip"
    layer_zstd = f"{_type_oci}.image.layer.v1.tar+zstd"


def annotation(name: str) -> None:
    return field(name=f"org.opencontainers.image.annotation.{name}", default=None)


class ImageAnnotation(Struct):
    created: str | None = annotation("created")
    authors: str | None = annotation("authors")
    url: str | None = annotation("url")
    documentation: str | None = annotation("documentation")
    source: str | None = annotation("source")
    version: str | None = annotation("version")
    revision: str | None = annotation("revision")
    vendor: str | None = annotation("vendor")
    licenses: str | None = annotation("licenses")
    ref_name: str | None = annotation("ref.name")
    title: str | None = annotation("title")
    description: str | None = annotation("description")
    base_image_digest: str | None = annotation("base.digest")
    base_image_name: str | None = annotation("base.name")


ImageAnnotation()
