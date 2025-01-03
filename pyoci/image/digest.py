from typing import Annotated

from msgspec import Meta

Digest = Annotated[  # TODO replace with object
    str,
    Meta(
        description="the cryptographic checksum digest of the object, in the pattern '<algorithm>:<encoded>'",
        pattern="^[a-z0-9]+(?:[+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+$",
    ),
]
