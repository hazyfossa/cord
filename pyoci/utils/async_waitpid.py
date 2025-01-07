# This is a huge hack to work around https://github.com/python/cpython/issues/119710
from asyncio import AbstractEventLoop, Future
from asyncio.subprocess import Process, SubprocessStreamProtocol
from asyncio.base_subprocess import BaseSubprocessTransport


class ExitNotifyStreamProtocol(SubprocessStreamProtocol):
    def __init__(self, limit: int, loop: AbstractEventLoop) -> None:
        super().__init__(limit, loop)
        self._exit_waiters: list[Future] = []

    def process_exited(self) -> None:
        return super().process_exited()


def waitpid(process: Process) -> None:
    transport: BaseSubprocessTransport = process._transport  # type: ignore # acessing private attribute
