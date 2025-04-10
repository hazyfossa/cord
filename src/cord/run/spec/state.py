from typing import TYPE_CHECKING, Annotated, Literal

from msgspec import Meta

from cord.base_types import UNSET, Annotations, Unset
from cord.base_types import Struct
from cord.oci.runtime import __oci_version__

Status = Literal["creating", "created", "running", "stopped"]


class State(Struct):
    id: str
    status: Status
    bundle: str

    pid: Annotated[int, Meta(ge=0)] | Unset = UNSET
    annotations: Annotations | Unset = UNSET

    if not TYPE_CHECKING:
        ociVersion: str = __oci_version__
