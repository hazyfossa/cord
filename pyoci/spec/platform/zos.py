from collections.abc import Sequence

from pyoci.spec.common import Struct
from pyoci.spec.platform.linux.devices import Device


class Zos(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-zos.md
    """

    devices: Sequence[Device] | None = None
