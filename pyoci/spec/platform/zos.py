from collections.abc import Sequence

from pyoci.spec.common import Struct
from pyoci.spec.platform.linux.devices import Device


class Zos(Struct):
    """
    z/OS platform-specific configurations
    """

    devices: Sequence[Device] | None = None
