import os
import stat
from collections.abc import Sequence
from enum import StrEnum
from typing import Annotated

from msgspec import Meta

from pyoci.base_types import GID, UID, Int64, Uint16, Uint64
from pyoci.common import UNSET, Struct, Unset
from pyoci.runtime.config.filesystem import FilePath

Major = Annotated[Int64, Meta(description="major device number")]
Minor = Annotated[Int64, Meta(description="minor device number")]

FileMode = Annotated[
    int,
    Meta(description="File permissions mode (typically an octal value)", ge=0, le=512),
]


class FileType(StrEnum):
    CHAR = "c"
    CHAR_u = "u"  # NOTE: This is an alias, it is literally identical to "c". # TODO: is this a problem somewhere?
    BLOCK = "b"
    FIFO = "p"

    @classmethod
    def from_stat(cls, stat_result: os.stat_result) -> "FileType":
        match stat.S_IFMT(stat_result.st_mode):
            case stat.S_IFBLK:
                return FileType.BLOCK
            case stat.S_IFCHR:
                return FileType.CHAR
            case stat.S_IFIFO:
                return FileType.FIFO
            case _:
                raise ValueError("Not a device")


class Device(Struct):
    type: FileType
    path: FilePath
    fileMode: FileMode | Unset = UNSET
    major: Major | Unset = UNSET
    minor: Minor | Unset = UNSET
    uid: UID | Unset = UNSET
    gid: GID | Unset = UNSET

    @classmethod
    def from_file(cls, path: str) -> "Device":
        info = os.lstat(path)

        return cls(
            type=FileType.from_stat(info),
            path=path,
            fileMode=info.st_mode,
            major=os.major(info.st_rdev),
            minor=os.minor(info.st_rdev),
        )
        # NOTE: uid and gid are not set here, a caller can set them if needed


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
