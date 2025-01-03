from typing import TYPE_CHECKING, Annotated, Literal
from msgspec import Meta

from pyoci.config import Annotations
from pyoci.common import Struct
from pyoci.version_utils import versioned

Status = Literal["creating", "created", "running", "stopped"]


@versioned
class State(Struct):
    if not TYPE_CHECKING:
        ociVersion: str

    id: str
    status: Status
    bundle: str
    pid: Annotated[int, Meta(ge=0)] | None = None
    annotations: Annotations | None = None
