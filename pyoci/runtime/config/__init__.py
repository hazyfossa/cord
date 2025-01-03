from collections.abc import Sequence
from typing import TYPE_CHECKING

from pyoci.base_types import Annotations
from pyoci.runtime import __oci_version__

from pyoci.common import Struct, const_field
from pyoci.runtime.config.filesystem import Mount, Root
from pyoci.runtime.config.hooks import Hooks
from pyoci.runtime.config.platform.linux import Linux
from pyoci.runtime.config.platform.solaris import Solaris
from pyoci.runtime.config.platform.vm import Vm
from pyoci.runtime.config.platform.windows import Windows
from pyoci.runtime.config.platform.zos import Zos
from pyoci.runtime.config.process import Process


@const_field("ociVersion", __oci_version__)
class Container(Struct):
    if not TYPE_CHECKING:
        ociVersion: str

    hooks: Hooks | None = None
    annotations: Annotations | None = None
    hostname: str | None = None
    domainname: str | None = None
    mounts: Sequence[Mount] | None = None
    root: Root | None = None
    process: Process | None = None

    linux: Linux | None = None
    solaris: Solaris | None = None
    windows: Windows | None = None
    vm: Vm | None = None
    zos: Zos | None = None
