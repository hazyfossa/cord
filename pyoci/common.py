from functools import partial
from typing import Mapping, TypeVar, TYPE_CHECKING
from msgspec import Struct

if not TYPE_CHECKING:

    class Struct(
        Struct, omit_defaults=True
    ): ...  # Do not write any of the default None configs, as they aren't necessary and take up space.

    # It would be better to avoid the placeholders completely, but that breaks python's dataclasses
    # so we need to specify each field as optional manually like this ": x | None = None"

T = TypeVar("T")  # TODO ref-py-3.13


def versioned(oci_version: str):
    def wrapper(struct: T) -> T:
        return partial(struct, ociVersion=oci_version)  # type: ignore

    return wrapper


Annotations = Mapping[str, str]
