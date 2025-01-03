from collections.abc import Sequence

from pyoci.common import Struct
from pyoci.base_types import Annotations
from .linux_features import LinuxFeatures


class Features(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/features.md

    Features of the pyoci.runtime. Unrelated to features of the host.
    None means "unknown", not "unsupported".
    """

    ociVersionMin: str
    ociVersionMax: str
    hooks: Sequence[str] | None = None
    mountOptions: Sequence[str] | None = None
    annotations: Annotations | None = None
    potentiallyUnsafeConfigAnnotations: Sequence[str] | None = None  # ?
    linux: LinuxFeatures | None = None
