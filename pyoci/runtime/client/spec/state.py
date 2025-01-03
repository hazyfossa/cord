from typing import TYPE_CHECKING, Annotated, Literal

from msgspec import Meta

from pyoci.base_types import Annotations
from pyoci.common import Struct, versioned
from pyoci.runtime import __oci_version__

Status = Literal["creating", "created", "running", "stopped"]


@versioned(__oci_version__)
class State(Struct):
    if not TYPE_CHECKING:
        ociVersion: str

    id: str
    status: Status
    bundle: str
    pid: Annotated[int, Meta(ge=0)] | None = None
    annotations: Annotations | None = None
