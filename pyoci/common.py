from functools import partial
from typing import TypeVar, TYPE_CHECKING, Any
from msgspec import Struct

if not TYPE_CHECKING:

    class Struct(
        Struct, omit_defaults=True
    ): ...  # Do not write any of the default None configs, as they aren't necessary and take up space.

    # It would be better to avoid the placeholders completely, but that breaks python's dataclasses
    # so we need to specify each field as optional manually like this ": x | None = None"

T = TypeVar("T")  # TODO ref-py-3.13


def const_field(field: str, value: Any):  # TODO check on deserialization.
    """
    Important: Don't forget to add the field to the Struct
    with 'if not TYPE_CHECKING: field: {type}'
    """

    def wrapper(struct: T) -> T:
        return partial(struct, **{field: value})  # type: ignore

    return wrapper
