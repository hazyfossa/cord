from collections.abc import Sequence
from typing import Annotated

from msgspec import Meta

from cord.base_types import UNSET, Unset
from cord.base_types import Struct
from cord.oci.runtime.filesystem import FilePath
from cord.oci.runtime.process import Env


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
