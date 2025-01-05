from pyoci.common import Struct, Unset, UNSET

# TODO better integration?


class Platform(Struct):
    architecture: str
    os: str
    os_version: str | Unset = UNSET
    os_features: list[str] | Unset = UNSET
    variant: str | Unset = UNSET
