from enum import StrEnum, auto
import platform
from typing import Self
from msgspec import field

from pyoci.common import UNSET, Struct, Unset


class Architecture(StrEnum):
    """
    GOARCH
    https://golang.org/doc/install/source#environment
    """

    arm = auto()
    arm64 = auto()
    amd64 = auto()
    i386 = auto()
    wasm = auto()
    loong64 = auto()
    mips = auto()
    mipsle = auto()
    mips64 = auto()
    mips64le = auto()
    ppc64 = auto()
    ppc64le = auto()
    riscv64 = auto()
    s390x = auto()

    @classmethod
    def current(cls) -> Self:
        # TODO: test for Go compatibility
        return cls(platform.machine())


class Os(StrEnum):
    """
    GOOS
    https://golang.org/doc/install/source#environment
    """

    aix = auto()
    android = auto()
    darwin = auto()
    dragonfly = auto()
    freebsd = auto()
    illumos = auto()
    ios = auto()
    js = auto()
    linux = auto()
    netbsd = auto()
    openbsd = auto()
    plan9 = auto()
    solaris = auto()
    wasip1 = auto()
    windows = auto()

    @classmethod
    def current(cls) -> Self:
        # TODO: test for Go compatibility
        return cls(platform.system().lower())


# TODO: support platform (cpu) variants


class Platform(Struct):
    architecture: Architecture | str
    os: Os | str
    os_version: str | Unset = field(name="os.version", default=UNSET)
    # TODO: are there any well-known values for os features?
    os_features: list[str] | Unset = field(name="os.features", default=UNSET)
    variant: str | Unset = UNSET

    @classmethod
    def current(cls) -> Self:
        return cls(
            architecture=Architecture.current(),
            os=Os.current(),
            os_version=platform.version(),
        )
