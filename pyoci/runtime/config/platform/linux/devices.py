from collections.abc import Sequence
from typing import Annotated

from msgspec import Meta

from pyoci.common import Struct, Unset, UNSET
from pyoci.base_types import GID
from pyoci.runtime.config.filesystem import FilePath
from pyoci.base_types import UID, Int64, Uint16, Uint64

Major = Annotated[Int64, Meta(description="major device number")]
Minor = Annotated[Int64, Meta(description="minor device number")]

FileMode = Annotated[
    int,
    Meta(description="File permissions mode (typically an octal value)", ge=0, le=512),
]

FileType = Annotated[
    str,
    Meta(description="Type of a block or special character device", pattern="^[cbup]$"),
]


class Device(Struct):
    type: FileType
    path: FilePath
    fileMode: FileMode | Unset = UNSET
    major: Major | Unset = UNSET
    minor: Minor | Unset = UNSET
    uid: UID | Unset = UNSET
    gid: GID | Unset = UNSET


class DeviceCgroup(Struct):
    allow: bool
    type: str | Unset = UNSET
    major: Major | Unset = UNSET
    minor: Minor | Unset = UNSET
    access: str | Unset = UNSET


class BlockIODevice(Struct):
    major: Major
    minor: Minor


class BlockIODeviceThrottle(BlockIODevice):
    rate: Uint64 | Unset = UNSET


Weight = Uint16


class BlockIODeviceWeight(BlockIODevice):
    weight: Weight | Unset = UNSET
    leafWeight: Weight | Unset = UNSET


class BlockIO(Struct):
    weight: Weight | Unset = UNSET
    leafWeight: Weight | Unset = UNSET
    throttleReadBpsDevice: Sequence[BlockIODeviceThrottle] | Unset = UNSET
    throttleWriteBpsDevice: Sequence[BlockIODeviceThrottle] | Unset = UNSET
    throttleReadIOPSDevice: Sequence[BlockIODeviceThrottle] | Unset = UNSET
    throttleWriteIOPSDevice: Sequence[BlockIODeviceThrottle] | Unset = UNSET
    weightDevice: Sequence[BlockIODeviceWeight] | Unset = UNSET
