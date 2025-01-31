from hashlib import new as new_hash
from typing import Annotated, Self

from msgspec import Meta

DigestStr = Annotated[
    str,
    Meta(
        pattern="^[a-z0-9]+(?:[+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+$",
    ),
]


class Digest:
    def __init__(self, algorithm: str, data: str) -> None:
        self.algorithm = algorithm
        self.data = data

    @classmethod
    def from_str(cls, digest: DigestStr) -> Self:
        return cls(*digest.split(":", 1))

    def __str__(self) -> DigestStr:
        return f"{self.algorithm}:{self.data}"

    def __eq__(self, digest) -> bool:
        assert isinstance(digest, Digest)
        return self.algorithm == digest.algorithm and self.data == digest.data

    @classmethod
    def from_bytes(cls, algorithm: str, data: bytes) -> Self:
        digest = new_hash(algorithm, data).hexdigest()
        return cls(algorithm, digest)

    @classmethod
    def from_file(cls, algorithm: str, path: str, buf_size: int = 4096) -> Self:
        digest = new_hash(algorithm)
        buf = bytearray(buf_size)
        view = memoryview(buf)

        with open(path, "rb") as f:
            while True:
                size = f.readinto(buf)
                if size == 0:
                    break

                digest.update(view[:size])

            return cls(algorithm, digest.hexdigest())
