from collections.abc import Sequence

from pyoci.common import Struct, Unset, UNSET
from pyoci.runtime.config.platform.linux import NamespaceType
from pyoci.runtime.config.platform.linux.seccomp import SeccompFeature
from pyoci.runtime.config.process import Capability


class Cgroup(Struct):
    v1: bool | Unset = UNSET
    v2: bool | Unset = UNSET
    systemd: bool | Unset = UNSET
    systemdUser: bool | Unset = UNSET
    rdma: bool | Unset = UNSET


class Feature(Struct):
    enabled: bool | Unset = UNSET


Apparmor = Feature
Selinux = Feature
IntelRdt = Feature
Idmap = Feature


class MountExtensions(Struct):
    idmap: Idmap | Unset = UNSET


class LinuxFeatures(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/features-linux.md
    """

    namespaces: Sequence[NamespaceType] | Unset = UNSET
    capabilities: Sequence[Capability] | Unset = UNSET
    cgroup: Cgroup | Unset = UNSET
    seccomp: SeccompFeature | Unset = UNSET
    apparmor: Apparmor | Unset = UNSET
    selinux: Selinux | Unset = UNSET
    intelRdt: IntelRdt | Unset = UNSET
    mountExtensions: MountExtensions | Unset = UNSET
