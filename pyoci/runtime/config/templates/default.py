from pyoci.runtime.config import Container
from pyoci.runtime.config.platform.linux import Namespace
from pyoci.runtime.config.platform.linux.devices import DeviceCgroup
from pyoci.runtime.config.process import Capabilities, Process, Rlimit
from pyoci.runtime.config.filesystem import Mount


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
