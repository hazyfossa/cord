from msgspec import Struct

from cord.base_types import UNSET, Annotations, Unset

from cord.oci.runtime.filesystem import Mount as OCIMount
from cord.oci.runtime.hooks import Hook as OCIHook
from cord.oci.runtime.platform.linux import IntelRdt as IntelRdt  # NOTE: same
from cord.oci.runtime.platform.linux.devices import Device as OCIDevice


class DeviceNode(OCIDevice):
    hostPath: str | Unset = UNSET
    permissions: str | Unset = UNSET

    def to_oci(self) -> OCIDevice:
        return OCIDevice(
            path=self.path,
            type=self.type,
            major=self.major,
            minor=self.minor,
            fileMode=self.fileMode,
            uid=self.uid,
            gid=self.gid,
        )


class Hook(OCIHook):
    hookName: str | Unset = UNSET  # TODO: not-unset, actually

    def to_oci(self) -> OCIHook:
        return OCIHook(
            path=self.path,
            args=self.args,
            env=self.env,
            timeout=self.timeout,
        )


class Mount(Struct):
    hostPath: str
    containerPath: str
    options: list[str] | Unset = UNSET
    type: str | Unset = UNSET

    def to_oci(self) -> OCIMount:
        return OCIMount(
            destination=self.containerPath,
            source=self.hostPath,
            options=self.options,
            type=self.type,
        )


class ContainerEdits(Struct):
    env: list[str] | Unset = UNSET
    deviceNodes: list[DeviceNode] | Unset = UNSET
    hooks: list[Hook] | Unset = UNSET
    mounts: list[Mount] | Unset = UNSET
    intelRdt: IntelRdt | Unset = UNSET
    additionalGids: list[int] | Unset = UNSET


class Device(Struct):
    name: str
    containerEdits: ContainerEdits

    annotations: Annotations | Unset = UNSET


class CDISpec(Struct):
    version: str
    kind: str

    devices: list[Device]
    annotations: Annotations | Unset = UNSET
    containerEdits: ContainerEdits | Unset = UNSET
