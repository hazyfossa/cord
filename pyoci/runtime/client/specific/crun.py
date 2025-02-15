from datetime import datetime
from pathlib import Path

from msgspec import field
from pyoci.common import Unset, UNSET
from pyoci.runtime.client.spec.state import State as BaseState


class ListEntry(
    BaseState
):  # NOTE: When listing, crun provides more than the spec, but less than "state"
    created: datetime | Unset = UNSET
    owner: str | Unset = UNSET


class State(ListEntry):
    _rootfs: str | None = field(name="rootfs", default=None)
    systemd_scope: str | Unset = UNSET

    # TODO: This may be wrong actually
    @property
    def rootfs(self) -> str | None:  # This exists so this mirrors the behaviour of runc
        if self._rootfs is not None:
            return str(Path(self.bundle) / self._rootfs)
