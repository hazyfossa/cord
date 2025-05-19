from collections.abc import Sequence

from cord.base_types import UNSET, Unset
from cord.base_types import Struct
from cord.oci.runtime.platform.linux import NamespaceType
from cord.oci.runtime.platform.linux.seccomp import SeccompFeature
from cord.oci.runtime.process import Capability


class Cgroup(Struct):
    v1: bool | Unset = UNSET
    v2: bool | Unset = UNSET
    systemd: bool | Unset = UNSET
    systemdUser: bool | Unset = UNSET
    rdma: bool | Unset = UNSET


class Feature(Struct):
    enabled: bool | Unset = UNSET


class MountExtensions(Struct):
    idmap: Feature | Unset = UNSET


class LinuxFeatures(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/features-linux.md
    """

    namespaces: Sequence[NamespaceType] | Unset = UNSET
    capabilities: Sequence[Capability] | Unset = UNSET
    cgroup: Cgroup | Unset = UNSET
    seccomp: SeccompFeature | Unset = UNSET
    apparmor: Feature | Unset = UNSET
    selinux: Feature | Unset = UNSET
    intelRdt: Feature | Unset = UNSET
    mountExtensions: MountExtensions | Unset = UNSET
