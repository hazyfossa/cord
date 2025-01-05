from multiprocessing import Value
from subprocess import CompletedProcess
from typing import Literal
import msgspec


class LogEntry(msgspec.Struct):  # not pyoci.common.Struct, as all fileds are required
    level: Literal["debug", "info", "warn", "error"]
    message: str
    time: str  # Do we need datetime parsing here?


def handle(result: CompletedProcess, **kwargs):
    if result.returncode == 0:
        return

    log = msgspec.json.decode(result.stderr, type=list[LogEntry])

    for entry in log:
        if entry.level == "error":
            match entry.message:
                case "container does not exist":
                    raise ValueError("Container {id} does not exist".format(**locals()))
