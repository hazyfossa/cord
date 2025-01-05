from collections.abc import Sequence
from typing import TYPE_CHECKING

from pyoci.base_types import Annotations
from pyoci.common import UNSET, Struct, Unset
from pyoci.runtime import __oci_version__
from pyoci.runtime.config.filesystem import Mount, Root
from pyoci.runtime.config.hooks import Hooks
from pyoci.runtime.config.platform.linux import Linux
from pyoci.runtime.config.platform.solaris import Solaris
from pyoci.runtime.config.platform.vm import Vm
from pyoci.runtime.config.platform.windows import Windows
from pyoci.runtime.config.platform.zos import Zos
from pyoci.runtime.config.process import Process


class Container(Struct):
    if not TYPE_CHECKING:
        ociVersion: str = __oci_version__

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
