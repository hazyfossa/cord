from datetime import datetime

from pyoci.common import UNSET, Unset
from pyoci.runtime import __oci_version__
from pyoci.runtime.client.spec.state import State as BaseState


class State(BaseState):
    rootfs: str | Unset = UNSET
    created: datetime | Unset = UNSET
    owner: str | Unset = UNSET
