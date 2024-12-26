__spec_version__ = "1.2.0"

from collections.abc import Sequence

from pyoci.common import Annotations, Struct
from pyoci.config.filesystem import Mount, Root
from pyoci.config.platform.linux import Linux
from pyoci.config.platform.solaris import Solaris
from pyoci.config.platform.vm import Vm
from pyoci.config.platform.windows import Windows
from pyoci.config.platform.zos import Zos
from pyoci.config.process import Process
from pyoci.config.hooks import Hooks


class Container(Struct):
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
