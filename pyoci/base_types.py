from typing import Annotated, Any, Mapping

from msgspec import Meta

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

Uint16Pointer = Uint16 | None
Uint64Pointer = Uint64 | None

UID = Uint32
GID = Uint32

Data = Annotated[bytes, "Base64"]
StringPointer = str | None

MapStringObject = Mapping[str, Mapping[str, Any]]
Annotations = Mapping[str, str]
