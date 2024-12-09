from typing import Annotated, Literal
from msgspec import Meta

from pyoci.spec import Annotations
from pyoci.spec.common import Struct

Status = Literal["creating", "created", "running", "stopped"]


class State(Struct):
    ociVersion: str
    id: str
    status: Status
    bundle: str
    pid: Annotated[int, Meta(ge=0)] | None = None
    annotations: Annotations | None = None
