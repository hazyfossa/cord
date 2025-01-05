from datetime import datetime
from pathlib import Path

from msgspec import field
from pyoci.common import const_field
from pyoci.runtime import __oci_version__
from pyoci.runtime.client.spec.state import BaseState


@const_field("ociVersion", __oci_version__)
class State(BaseState):
    rootfs: str | None = None
    created: datetime | None = None
    owner: str | None = None
