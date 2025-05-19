from collections.abc import Sequence

from cord.base_types import Struct
from cord.base_types import UNSET, Annotations, Unset
from .linux_features import LinuxFeatures


class Features(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/features.md

    Features of the runtime. Unrelated to features of the host.
    Unset means "unknown", not "unsupported".
    """

    ociVersionMin: str
    ociVersionMax: str
    hooks: Sequence[str] | Unset = UNSET
    mountOptions: Sequence[str] | Unset = UNSET
    annotations: Annotations | Unset = UNSET
    potentiallyUnsafeConfigAnnotations: Sequence[str] | Unset = UNSET
    linux: LinuxFeatures | Unset = UNSET
