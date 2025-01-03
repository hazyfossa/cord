from pyoci.common import Struct

# TODO better integration?


class Platform(Struct):
    architecture: str
    os: str
    os_version: str | None = None
    os_features: list[str] | None = None
    variant: str | None = None
