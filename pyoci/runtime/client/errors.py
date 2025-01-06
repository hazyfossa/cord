from asyncio import StreamReader
from typing import Literal
import msgspec


class ContainerRuntimeError(RuntimeError): ...


class LogEntry(msgspec.Struct):
    level: Literal["debug", "info", "warn", "error"]
    message: str = msgspec.field(name="msg")
    time: str  # Do we need datetime parsing here?


decoder = msgspec.json.Decoder(LogEntry)


async def handle(stderr: StreamReader | None) -> None:
    if stderr is None:
        raise ContainerRuntimeError(
            "Container runtime failed. Cannot provide an error, stderr isn't captured."
        )

    log = decoder.decode_lines(await stderr.read())

    for entry in log:
        if entry.level == "error":  # TODO: Do we always see at-most one error?
            raise ContainerRuntimeError(entry.message)
