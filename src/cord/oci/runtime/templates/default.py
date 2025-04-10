from collections.abc import Sequence
from copy import deepcopy

from msgspec import field

from cord.base_types import Unset
from cord.base_types import Struct
from cord.oci.runtime import ContainerConfig as BaseContainerConfig
from cord.oci.runtime.filesystem import Mount, Root
from cord.oci.runtime.platform.linux import (
    Linux as BaseLinux,
)
from cord.oci.runtime.platform.linux import (
    Namespace,
    RootfsPropagation,
)
from cord.oci.runtime.platform.linux import (
    Resources as BaseResources,
)
from cord.oci.runtime.platform.linux.devices import DeviceCgroup
from cord.oci.runtime.platform.linux.seccomp import Seccomp
from cord.oci.runtime.process import (
    Capabilities,
    Rlimit,
    User,
)
from cord.oci.runtime.process import (
    Process as BaseProcess,
)

# TODO: consider merging with relevant files, or even replacing defaults in base structs with these

mounts = [
    Mount(
        destination="/proc",
        type="proc",
        source="proc",
        options=["nosuid", "noexec", "nodev"],
    ),
    Mount(
        destination="/dev",
        type="tmpfs",
        source="tmpfs",
        options=["nosuid", "strictatime", "mode=755", "size=65536k"],
    ),
    Mount(
        destination="/dev/pts",
        type="devpts",
        source="devpts",
        options=[
            "nosuid",
            "noexec",
            "newinstance",
            "ptmxmode=0666",
            "mode=0620",
            "gid=5",
        ],
    ),
    Mount(
        destination="/dev/shm",
        type="tmpfs",
        source="shm",
        options=["nosuid", "noexec", "nodev", "mode=1777", "size=65536k"],
    ),
    Mount(
        destination="/dev/mqueue",
        type="mqueue",
        source="mqueue",
        options=["nosuid", "noexec", "nodev"],
    ),
    Mount(
        destination="/sys",
        type="sysfs",
        source="sysfs",
        options=["nosuid", "noexec", "nodev", "ro"],
    ),
    Mount(
        destination="/run",
        type="tmpfs",
        source="tmpfs",
        options=["nosuid", "strictatime", "mode=755", "size=65536k"],
    ),
]

# TODO: consider a toggle-able struct
namespaces = [
    Namespace("pid"),
    Namespace("ipc"),
    Namespace("uts"),
    Namespace("mount"),
    Namespace("network"),
]

rootfs = "rootfs"

_default_unix_capabilities = [
    "CAP_CHOWN",
    "CAP_DAC_OVERRIDE",
    "CAP_FSETID",
    "CAP_FOWNER",
    "CAP_MKNOD",
    "CAP_NET_RAW",
    "CAP_SETGID",
    "CAP_SETUID",
    "CAP_SETFCAP",
    "CAP_SETPCAP",
    "CAP_NET_BIND_SERVICE",
    "CAP_SYS_CHROOT",
    "CAP_KILL",
    "CAP_AUDIT_WRITE",
]

capabilities = Capabilities(
    bounding=_default_unix_capabilities,
    permitted=_default_unix_capabilities,
    effective=_default_unix_capabilities,
    inheritable=_default_unix_capabilities,
)

rlimits = [Rlimit("RLIMIT_NOFILE", 1024, 1024)]

masked_paths = [
    "/proc/acpi",
    "/proc/asound",
    "/proc/kcore",
    "/proc/keys",
    "/proc/latency_stats",
    "/proc/timer_list",
    "/proc/timer_stats",
    "/proc/sched_debug",
    "/sys/firmware",
    "/sys/devices/virtual/powercap",
    "/proc/scsi",
]

readonly_paths = [
    "/proc/bus",
    "/proc/fs",
    "/proc/irq",
    "/proc/sys",
    "/proc/sysrq-trigger",
]

devices = [
    DeviceCgroup(allow=False, access="rwm"),
]

root_user = User(uid=0, gid=0)

env_path = "/usr/local/bin:/usr/bin:/bin"  # TODO


def default[T](obj: T) -> T:
    return field(default_factory=lambda: deepcopy(obj))


def default_struct[T: Struct](obj: type[T]) -> T:
    return field(default_factory=lambda: obj())


class Process(BaseProcess, Struct):
    cwd: str = "/"
    user: User | Unset = default(root_user)
    noNewPrivileges: bool | Unset = True
    capabilities: Capabilities | Unset = default(capabilities)

    def __post_init__(self):
        self.env = (self.env or []) + [f"PATH={env_path}"]

        if self.terminal:
            self.env.append("TERM=xterm")


class Resources(BaseResources, Struct):
    devices: Sequence[DeviceCgroup] | Unset = default(devices)


class Linux(BaseLinux, Struct):
    namespaces: Sequence[Namespace] | Unset = default(namespaces)
    rootfsPropagation: RootfsPropagation | Unset = "private"
    maskedPaths: Sequence[str] | Unset = default(masked_paths)
    readonlyPaths: Sequence[str] | Unset = default(readonly_paths)
    resources: BaseResources | Unset = default_struct(Resources)


class ContainerConfig(BaseContainerConfig, Struct):
    root: Root | Unset = default(Root(path=rootfs))
    mounts: Sequence[Mount] | Unset = default(mounts)
    process: BaseProcess | Unset = default_struct(Process)
    linux: BaseLinux | Unset = default_struct(Linux)
