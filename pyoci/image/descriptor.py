from collections.abc import Sequence

# TODO: consider using pathlib
from os import stat

from msgspec import field

from pyoci.base_types import Annotations, Data, Int64
from pyoci.common import UNSET, Struct, Unset
from pyoci.image.digest import Digest, DigestStr
from pyoci.image.platform import Platform
from pyoci.image.well_known import MediaType, OciMediaType


class Descriptor(Struct):
    """
    https://github.com/opencontainers/image-spec/blob/v1.1.0/descriptor.md
    """

    size: Int64  # in bytes
    digest: DigestStr

    urls: Sequence[str] | Unset = UNSET
    embedded_data: Data | Unset = field(name="data", default=UNSET)
    artifactType: MediaType | Unset = UNSET
    annotations: Annotations | Unset = UNSET

    mediaType: str = OciMediaType.content_descriptor

    def validate_data(self, data: bytes) -> bool:
        descriptor_digest = Digest.from_str(self.digest)
        data_digest = Digest.from_bytes(descriptor_digest.algorithm, data)

        return descriptor_digest == data_digest and len(data) == self.size

    # TODO: consider dynamic buffer sizes based on descriptor size
    def validate_file(self, path: str, buf_size: int = 4096) -> bool:
        descriptor_digest = Digest.from_str(self.digest)
        data_digest = Digest.from_file(descriptor_digest.algorithm, path, buf_size)

        return descriptor_digest == data_digest and self.size == stat(path).st_size


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
    size=2, embedded_data=b"{}", digest=_EMPTY_DIGEST, mediaType=OciMediaType.empty
)


# NOTE: Not part of the specification, used here for stronger typing
class ManifestDescriptor(Descriptor):
    platform: Platform | Unset = UNSET


# TODO: consider typed classes, one per descriptor type. ConfigDescriptor, Layer, etc.
# Or, maybe, only get instances of ContentDescriptor's from relevant classes. So, ImageConfig.descriptor()
# In that case, we'll need make those structs generic over mediaType and annotate the descriptor fields with DescriptorFor[...]
