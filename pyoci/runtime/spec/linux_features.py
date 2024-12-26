from collections.abc import Sequence
from typing import Annotated

from msgspec import Meta

from pyoci.spec.common import Struct
from pyoci.spec.platform.linux.main import NamespaceType
from pyoci.spec.platform.linux.seccomp import SeccompFeature

Capability = Annotated[str, Meta(pattern="^CAP_[A-Z_]+$")]  # TODO does this need to be strict? Performance impact?


class Cgroup(Struct):
    v1: bool | None = None
    v2: bool | None = None
    systemd: bool | None = None
    systemdUser: bool | None = None
    rdma: bool | None = None


class Feature(Struct):
    enabled: bool | None = None


Apparmor = Feature
Selinux = Feature
IntelRdt = Feature
Idmap = Feature


class MountExtensions(Struct):
    idmap: Idmap | None = None


class LinuxFeatures(Struct):
    """
    https://github.com/opencontainers/runtime-spec/blob/main/features-linux.md
    """
    namespaces: Sequence[NamespaceType] | None = None
    capabilities: Sequence[Capability] | None = None
    cgroup: Cgroup | None = None
    seccomp: SeccompFeature | None = None
    apparmor: Apparmor | None = None
    selinux: Selinux | None = None
    intelRdt: IntelRdt | None = None
    mountExtensions: MountExtensions | None = None
