from collections.abc import Sequence
from typing import Literal

from cord.base_types import UNSET, Unset
from cord.base_types import Struct
from cord.oci.runtime.filesystem import FilePath

RootImageFormat = Literal["raw", "qcow2", "vdi", "vmdk", "vhd"]


class Image(Struct):
    path: FilePath
    format: RootImageFormat


class Hypervisor(Struct):
    path: FilePath
    parameters: Sequence[str] | Unset = UNSET


class Kernel(Struct):
    path: FilePath
    parameters: Sequence[str] | Unset = UNSET
    initrd: FilePath | Unset = UNSET


class Vm(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-vm.md
    """

    kernel: Kernel
    hypervisor: Hypervisor | Unset = UNSET
    image: Image | Unset = UNSET
