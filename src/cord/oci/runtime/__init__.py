from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from cord.base_types import UNSET, Annotations, Struct, Unset
from cord.utils.jsonstruct import JsonStruct

from .filesystem import Mount, Root
from .hooks import Hooks
from .platform.linux import Linux
from .platform.solaris import Solaris
from .platform.vm import Vm
from .platform.windows import Windows
from .platform.zos import Zos
from .process import Process

__oci_version__ = "1.2.0"


class ContainerConfig(Struct, JsonStruct):
    process: Process | Unset = UNSET
    mounts: Sequence[Mount] | Unset = UNSET
    hostname: str | Unset = UNSET
    domainname: str | Unset = UNSET
    root: Root | Unset = UNSET

    linux: Linux | Unset = UNSET
    solaris: Solaris | Unset = UNSET
    windows: Windows | Unset = UNSET
    vm: Vm | Unset = UNSET
    zos: Zos | Unset = UNSET

    hooks: Hooks | Unset = UNSET
    annotations: Annotations | Unset = UNSET

    if not TYPE_CHECKING:
        ociVersion: str = __oci_version__

    def read_bundle(self, bundle: Path) -> None:
        self.loads((bundle / "config.json").read_bytes())

    def write_bundle(self, bundle: Path) -> None:
        (bundle / "config.json").write_bytes(self.dumps())
