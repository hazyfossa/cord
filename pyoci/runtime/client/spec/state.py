from typing import TYPE_CHECKING, Annotated, Literal

from msgspec import Meta

from pyoci.base_types import Annotations
from pyoci.common import Struct, Unset, UNSET
from pyoci.runtime import __oci_version__

Status = Literal["creating", "created", "running", "stopped"]


class State(Struct):
    id: str
    status: Status
    bundle: str

    if not TYPE_CHECKING:
        ociVersion: str = __oci_version__

    pid: Annotated[int, Meta(ge=0)] | Unset = UNSET
    annotations: Annotations | Unset = UNSET
