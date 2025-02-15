from collections.abc import Buffer
from typing import TYPE_CHECKING, Literal

from msgspec import Struct as Struct
from msgspec import json


class SimpleJsonMixin:
    @classmethod
    def loads(cls, data: Buffer | str):
        return json.decode(data, type=cls)

    def dumps(self) -> bytes:
        return json.encode(self)


if TYPE_CHECKING:
    #! This is a hack
    # This is needed for IDEs to recognize that bool(UNSET) is False when applying defaults.

    class Unset:
        def __bool__(self) -> Literal[False]: ...

    UNSET = Unset()

else:
    from msgspec import UNSET
    from msgspec import UnsetType as Unset
