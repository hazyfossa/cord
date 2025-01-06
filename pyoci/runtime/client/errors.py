from subprocess import CalledProcessError, CompletedProcess, Popen
from typing import Literal
import msgspec


class LogEntry(msgspec.Struct):
    level: Literal["debug", "info", "warn", "error"]
    message: str = msgspec.field(name="msg")
    time: str  # Do we need datetime parsing here?


decoder = msgspec.json.Decoder(LogEntry)


def handle(stderr: bytes) -> None:
    log = decoder.decode_lines(stderr)

    for entry in log:
        if entry.level == "error":  # TODO: Do we always see at-most one error?
            raise RuntimeError(entry.message)
