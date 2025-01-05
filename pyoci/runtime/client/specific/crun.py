from datetime import datetime
from pathlib import Path

from msgspec import field
from pyoci.common import const_field
from pyoci.runtime import __oci_version__
from pyoci.runtime.client.spec.state import BaseState


class ListEntry(
    BaseState
):  # When listing, crun provides more than the spec, but less than "state"
    created: datetime | None = None
    owner: str | None = None


@const_field("ociVersion", __oci_version__)
class State(ListEntry):
    _rootfs: str | None = field(name="rootfs", default=None)
    systemd_scope: str | None = None

    @property
    def rootfs(self) -> str | None:  # This exists so this mirrors the behaviour of runc
        if self._rootfs is not None:
            return str(Path(self.bundle) / self._rootfs)
