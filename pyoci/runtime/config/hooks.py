from collections.abc import Sequence
from typing import Annotated

from msgspec import Meta

from pyoci.common import Struct, Unset, UNSET
from pyoci.runtime.config.filesystem import FilePath
from pyoci.runtime.config.process import Env


class Hook(Struct):
    path: FilePath
    args: Sequence[str] | Unset = UNSET
    env: Env | Unset = UNSET
    timeout: Annotated[int, Meta(ge=1)] | Unset = UNSET


class Hooks(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/config.md#posix-platform-hooks
    """

    prestart: Sequence[Hook] | Unset = UNSET
    createRuntime: Sequence[Hook] | Unset = UNSET
    createContainer: Sequence[Hook] | Unset = UNSET
    startContainer: Sequence[Hook] | Unset = UNSET
    poststart: Sequence[Hook] | Unset = UNSET
    poststop: Sequence[Hook] | Unset = UNSET
