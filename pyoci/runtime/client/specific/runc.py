from datetime import datetime
from pathlib import Path

from msgspec import field
from pyoci.runtime import __oci_version__
from pyoci.common import Unset, UNSET
from pyoci.runtime.client.spec.state import State as BaseState


class State(BaseState):
    rootfs: str | Unset = UNSET
    created: datetime | Unset = UNSET
    owner: str | Unset = UNSET
