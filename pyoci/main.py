from collections.abc import Sequence

from msgspec import json

from pyoci.common import Annotations, Struct
from pyoci.filesystem import Mount, Root
from pyoci.platform.linux import Linux
from pyoci.platform.solaris import Solaris
from pyoci.platform.vm import Vm
from pyoci.platform.windows import Windows
from pyoci.platform.zos import Zos
from pyoci.process import Process
from pyoci.runtime_hooks import Hooks


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

    def spec(self) -> bytes:
        return json.encode(self)


def read_spec(spec: bytes | str) -> Container:
    return json.decode(spec, type=Container)
