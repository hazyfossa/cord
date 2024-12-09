__spec_version__ = "1.2.0"

from collections.abc import Sequence

from pyoci.spec.common import Annotations, Struct
from pyoci.spec.filesystem import Mount, Root
from pyoci.spec.platform.linux import Linux
from pyoci.spec.platform.solaris import Solaris
from pyoci.spec.platform.vm import Vm
from pyoci.spec.platform.windows import Windows
from pyoci.spec.platform.zos import Zos
from pyoci.spec.process import Process
from pyoci.spec.hooks import Hooks


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
