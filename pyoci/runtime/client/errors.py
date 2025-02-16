from subprocess import Popen
from typing import Any, Literal

import msgspec


class ContainerRuntimeError(RuntimeError): ...


class LogEntry(msgspec.Struct):
    level: Literal["debug", "info", "warn", "error"]
    message: str = msgspec.field(name="msg")
    time: str  # Do we need datetime parsing here?


decoder = msgspec.json.Decoder(LogEntry)


def handle(process: Popen, **context) -> None:
    ret = process.returncode
    if ret is None:
        raise RuntimeError(
            "Error handler called before waiting for the process to finish."
        )

    if ret == 0:
        return

    stderr = process.stderr  # TODO: errors without stderr

    if stderr is None:
        raise RuntimeError("Cannot handle errors as stderr isn't captured.")

    log = decoder.decode_lines(stderr.read())

    # TODO: Do we always see at-most one error?
    # TODO: parse messages for more pythonic errors

    for entry in log:
        if entry.level == "error":
            raise ContainerRuntimeError(entry.message)

    raise ContainerRuntimeError(
        f"Exited with code {ret}. Couldn't find an error in the log."
    )
