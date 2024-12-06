from collections.abc import Sequence

from pyoci.common import Struct
from pyoci.platform.linux.devices import Device


class Zos(Struct):
    """
    z/OS platform-specific configurations
    """

    devices: Sequence[Device] | None = None
