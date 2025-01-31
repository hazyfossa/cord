from collections.abc import Sequence
from typing import Self

from msgspec import field

from pyoci.base_types import Annotations, Data, Int64
from pyoci.common import UNSET, Struct, Unset
from pyoci.image.const import Architecture, MediaType, OciMediaType, Os
from pyoci.image.digest import Digest


class Descriptor(Struct):
    """
    https://github.com/opencontainers/image-spec/blob/v1.1.0/descriptor.md
    """

    size: Int64  # in bytes
    digest: Digest

    urls: Sequence[str] | Unset = UNSET
    data: Data | Unset = UNSET
    artifactType: MediaType | Unset = UNSET
    annotations: Annotations | Unset = UNSET

    mediaType: str = OciMediaType.content_descriptor


# class DescriptorMixin(Struct):
#     mediaType: str

#     @property
#     def descriptor(self) -> ContentDescriptor: ...


# This is a static pre-calculated value, as empty descriptors are so common for artifacts,
# that it'll probably need to be calculated on each import anyway
_EMPTY_DIGEST = (
    "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
)

EmptyDescriptor = Descriptor(
    size=2, data=b"{}", digest=_EMPTY_DIGEST, mediaType=OciMediaType.empty
)


class Platform(Struct):
    architecture: Architecture | str
    os: Os | str
    os_version: str | Unset = field(name="os.version", default=UNSET)
    # TODO: are there any well-known values for os features?
    os_features: list[str] | Unset = field(name="os.features", default=UNSET)
    variant: str | Unset = UNSET


# NOTE: Not part of the specification, used here for stronger typing
class ManifestDescriptor(Descriptor):
    platform: Platform | Unset = UNSET


# TODO: consider typed classes, one per descriptor type. ConfigDescriptor, Layer, etc.
# Or, maybe, only get instances of ContentDescriptor's from relevant classes. So, ImageConfig.descriptor()
# In that case, we'll need make those structs generic over mediaType and annotate the descriptor fields with DescriptorFor[...]
