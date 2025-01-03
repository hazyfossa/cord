from functools import partial
from typing import TypeVar

from . import __oci_version__

T = TypeVar("T")


def versioned(struct: T) -> T:
    return partial(struct, ociVersion=__oci_version__)  # type: ignore
