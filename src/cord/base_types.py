from typing import TYPE_CHECKING, Annotated, Final, Literal

from msgspec import Meta
from msgspec import Struct as Struct

# TODO: Add support for disabling these checks

Int8 = Annotated[int, Meta(ge=-128, le=127)]
Int16 = Annotated[int, Meta(ge=-32768, le=32767)]
Int32 = Annotated[int, Meta(ge=-2147483648, le=2147483647)]
Int64 = Annotated[int, Meta(ge=-9223372036854775808, le=9223372036854775807)]
Uint8 = Annotated[int, Meta(ge=0, le=255)]
Uint16 = Annotated[int, Meta(ge=0, le=65535)]
Uint32 = Annotated[int, Meta(ge=0, le=4294967295)]
# Uint64 = Annotated[int, Meta(ge=0, le=18446744073709551615)] Msgspec doesn't support 'le' on values that won't fit into Int64
Uint64 = Annotated[int, Meta(ge=0), "le=18446744073709551615"]

UID = Uint32
GID = Uint32

Data = Annotated[bytes, "Base64"]
Annotations = dict[str, str]


if TYPE_CHECKING:

    class Unset(Final):
        def __bool__(self) -> Literal[False]: ...

    #! This is a hack
    # This is needed for IDEs to recognize that bool(UNSET) is False when applying defaults.

    UNSET = Unset()
else:
    from msgspec import UNSET
    from msgspec import UnsetType as Unset
