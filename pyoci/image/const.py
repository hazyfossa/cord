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


class ImageAnnotation(Struct):
    created: str | None = field(
        name="org.opencontainers.image.created",
        default=None,
    )

    authors: str | None = field(
        name="org.opencontainers.image.authors",
        default=None,
    )

    url: str | None = field(
        name="org.opencontainers.image.url",
        default=None,
    )

    documentation: str | None = field(
        name="org.opencontainers.image.documentation",
        default=None,
    )

    source: str | None = field(
        name="org.opencontainers.image.source",
        default=None,
    )

    version: str | None = field(
        name="org.opencontainers.image.version",
        default=None,
    )

    revision: str | None = field(
        name="org.opencontainers.image.revision",
        default=None,
    )

    vendor: str | None = field(
        name="org.opencontainers.image.vendor",
        default=None,
    )

    licenses: str | None = field(
        name="org.opencontainers.image.licenses",
        default=None,
    )

    ref_name: str | None = field(
        name="org.opencontainers.image.ref.name",
        default=None,
    )

    title: str | None = field(
        name="org.opencontainers.image.title",
        default=None,
    )

    description: str | None = field(
        name="org.opencontainers.image.description",
        default=None,
    )

    base_image_digest: str | None = field(
        name="org.opencontainers.image.base.digest",
        default=None,
    )

    base_image_name: str | None = field(
        name="org.opencontainers.image.base.name",
        default=None,
    )
