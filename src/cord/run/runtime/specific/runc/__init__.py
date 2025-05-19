from datetime import datetime

from cord.base_types import Unset
from cord.base_types import UNSET
from cord.oci.runtime import __oci_version__
from cord.run.spec.state import State as BaseState


class State(BaseState):
    rootfs: str | Unset = UNSET
    created: datetime | Unset = UNSET
    owner: str | Unset = UNSET
