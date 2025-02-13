from collections.abc import Sequence

from msgspec import field

from pyoci.base_types import Annotations, Data, Int64
from pyoci.common import UNSET, Struct, Unset
from pyoci.image.digest import Digest, DigestStr
from pyoci.image.platform import Platform
from pyoci.image.well_known import MediaType, OciMediaType


class DescriptorValidationError(Exception): ...


class DescriptorSizeMismatch(DescriptorValidationError):
    def __init__(self, expected: int, actual: int) -> None:
        # TODO: human readable sizes
        super().__init__(
            f"Data size mismatch: expected (from descriptor) {expected}b, got {actual}b"
        )


class DescriptorDigestMismatch(DescriptorValidationError):
    def __init__(self, expected: Digest, actual: Digest) -> None:
        # TODO: human readable sizes
        super().__init__(
            f"Data digest mismatch: expected (from descriptor) '{expected}', got '{actual}'"
        )


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

    def validate(self, data: bytes | Digest, size: int) -> None:
        descriptor_digest = Digest.from_str(self.digest)

        if not isinstance(data, Digest):
            data = Digest.from_bytes(data, algorithm=descriptor_digest.algorithm)
        elif data.algorithm != descriptor_digest.algorithm:
            raise ValueError(
                "Cannot validate against a digest using a different algorithm"
            )

        data_digest = data  # NOTE: renaming

        if descriptor_digest != data_digest:
            raise DescriptorDigestMismatch(
                expected=descriptor_digest, actual=data_digest
            )

        if size != self.size:
            raise DescriptorSizeMismatch(expected=self.size, actual=size)


# class DescriptorMixin(Struct):
#     mediaType: str

#     @property
#     def descriptor(self) -> ContentDescriptor: ...


# NOTE: This is a static pre-calculated value, as empty descriptors are so common for artifacts,
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
