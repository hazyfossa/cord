from collections.abc import Sequence

from cord.base_types import UNSET, Unset
from cord.base_types import Struct
from cord.oci.runtime.platform.linux.devices import Device


class Zos(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config-zos.md
    """

    devices: Sequence[Device] | Unset = UNSET
