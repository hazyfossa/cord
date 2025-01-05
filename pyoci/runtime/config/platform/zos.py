from collections.abc import Sequence

from pyoci.common import Struct, Unset, UNSET
from pyoci.runtime.config.platform.linux.devices import Device


class Zos(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-zos.md
    """

    devices: Sequence[Device] | Unset = UNSET
