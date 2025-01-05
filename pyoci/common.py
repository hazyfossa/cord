from typing import TYPE_CHECKING, NewType, cast
from msgspec import Struct as Struct


if TYPE_CHECKING:
    #! This is a hack
    # This is needed for IDEs to recognize that bool(UNSET) is Flase when applying defaults.
    Unset = NewType("Unset", None)
    UNSET = cast(Unset, None)

else:
    from msgspec import UnsetType as Unset, UNSET
