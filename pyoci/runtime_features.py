from collections.abc import Sequence

from pyoci.common import Annotations, Struct
from pyoci.platform.linux.runtime_features import LinuxFeatures


class Features(Struct):
    ociVersionMin: str
    ociVersionMax: str
    hooks: Sequence[str] | None = None
    mountOptions: Sequence[str] | None = None
    annotations: Annotations | None = None
    potentiallyUnsafeConfigAnnotations: Sequence[str] | None = None
    linux: LinuxFeatures | None = None
