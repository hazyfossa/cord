from collections.abc import Sequence

from pyoci.common import Struct


class Capabilities(Struct):
    bounding: Sequence[str] | None = None
    permitted: Sequence[str] | None = None
    effective: Sequence[str] | None = None
    inheritable: Sequence[str] | None = None
    ambient: Sequence[str] | None = None
