from collections.abc import Sequence
from typing import TYPE_CHECKING, Mapping

from msgspec import Struct

from pyoci.spec.int_types import Uint32

if not TYPE_CHECKING:

    class Struct(
        Struct, omit_defaults=True
    ): ...  # Do not write any of the default None configs, as they aren't necessary and take up space.

    # It would be better to avoid the placeholders completely, but that breaks python's dataclasses
    # so we need to specify each field as optional manually like this ": x | None = None"


UID = Uint32

GID = Uint32

Env = Sequence[str]


class IDMapping(Struct):
    containerID: Uint32
    hostID: Uint32
    size: Uint32


Annotations = Mapping[str, str]
