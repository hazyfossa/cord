from enum import StrEnum, auto
from typing import Annotated
from msgspec import Meta, field
from pyoci.common import Struct, Unset, UNSET

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
# fmt: on


def _image_annotation(key: str) -> Unset:
    return field(name=f"org.opencontainers.image.annotation.{key}", default=UNSET)


class ImageAnnotations(Struct):
    created: str | Unset = _image_annotation("created")
    authors: str | Unset = _image_annotation("authors")
    url: str | Unset = _image_annotation("url")
    documentation: str | Unset = _image_annotation("documentation")
    source: str | Unset = _image_annotation("source")
    version: str | Unset = _image_annotation("version")
    revision: str | Unset = _image_annotation("revision")
    vendor: str | Unset = _image_annotation("vendor")
    licenses: str | Unset = _image_annotation("licenses")
    ref_name: str | Unset = _image_annotation("ref.name")
    title: str | Unset = _image_annotation("title")
    description: str | Unset = _image_annotation("description")
    base_image_digest: str | Unset = _image_annotation("base.digest")
    base_image_name: str | Unset = _image_annotation("base.name")


def _runtime_annotation(key: str) -> Unset:
    return field(name=f"org.opencontainers.image.{key}", default=UNSET)


# TODO
class RuntimeConfigAnnotations(Struct):
    os: str | Unset = _runtime_annotation("os")
    architecture: str | Unset = _runtime_annotation("architecture")


class Architecture(StrEnum):
    """
    GOARCH
    https://golang.org/doc/install/source#environment
    """

    arm = auto()
    arm64 = auto()
    amd64 = auto()
    i386 = auto()
    wasm = auto()
    loong64 = auto()
    mips = auto()
    mipsle = auto()
    mips64 = auto()
    mips64le = auto()
    ppc64 = auto()
    ppc64le = auto()
    riscv64 = auto()
    s390x = auto()


class Os(StrEnum):
    """
    GOOS
    https://golang.org/doc/install/source#environment
    """

    aix = auto()
    android = auto()
    darwin = auto()
    dragonfly = auto()
    freebsd = auto()
    illumos = auto()
    ios = auto()
    js = auto()
    linux = auto()
    netbsd = auto()
    openbsd = auto()
    plan9 = auto()
    solaris = auto()
    wasip1 = auto()
    windows = auto()
