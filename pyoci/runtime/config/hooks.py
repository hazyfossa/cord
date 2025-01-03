from collections.abc import Sequence
from typing import Annotated

from msgspec import Meta

from pyoci.common import Struct
from pyoci.runtime.config.filesystem import FilePath
from pyoci.runtime.config.process import Env


class Hook(Struct):
    path: FilePath
    args: Sequence[str] | None = None
    env: Env | None = None
    timeout: Annotated[int, Meta(ge=1)] | None = None


class Hooks(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#posix-platform-hooks
    """

    prestart: Sequence[Hook] | None = None
    createRuntime: Sequence[Hook] | None = None
    createContainer: Sequence[Hook] | None = None
    startContainer: Sequence[Hook] | None = None
    poststart: Sequence[Hook] | None = None
    poststop: Sequence[Hook] | None = None
