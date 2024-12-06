from collections.abc import Sequence
from typing import Literal

from pyoci.spec.common import Struct
from pyoci.spec.filesystem import FilePath

RootImageFormat = Literal["raw", "qcow2", "vdi", "vmdk", "vhd"]


class Image(Struct):
    path: FilePath
    format: RootImageFormat


class Hypervisor(Struct):
    path: FilePath
    parameters: Sequence[str] | None = None


class Kernel(Struct):
    path: FilePath
    parameters: Sequence[str] | None = None
    initrd: FilePath | None = None


class Vm(Struct):
    kernel: Kernel
    hypervisor: Hypervisor | None = None
    image: Image | None = None
