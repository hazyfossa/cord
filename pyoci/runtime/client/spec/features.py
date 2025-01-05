from collections.abc import Sequence

from pyoci.common import Struct, Unset, UNSET
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
    hooks: Sequence[str] | Unset = UNSET
    mountOptions: Sequence[str] | Unset = UNSET
    annotations: Annotations | Unset = UNSET
    potentiallyUnsafeConfigAnnotations: Sequence[str] | Unset = UNSET  # ?
    linux: LinuxFeatures | Unset = UNSET
