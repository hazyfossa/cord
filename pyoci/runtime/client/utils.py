# - default with encode=False is only for documentation
# (i.e. showing default values within a container runtime)
# - default with encode=True is a regular python default
from dataclasses import dataclass
from typing import BinaryIO


def default(value, encode=False):
    if encode:
        return value

    return None


@dataclass
class OpenIO:
    stdin: BinaryIO
    stdout: BinaryIO
    stderr: BinaryIO

    @property
    def as_tuple(self):
        return (self.stdin, self.stdout, self.stderr)

    def close(self) -> None:
        map(lambda x: x.close(), self.as_tuple)
