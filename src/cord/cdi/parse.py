import re
from typing import Literal, Protocol
from cord.base_types import Struct


class DeviceNameError(Exception):
    def __init__(
        self, name: str | None, reason: str | None = None, part: str | None = None
    ) -> None:
        if part is not None:
            reason = f"invalid {part}: {reason}"

        super().__init__(f"Invalid device name {name}: {reason}")


DEVICE_RE = re.compile(r"^(?P<vendor>[^/]+)/(?P<class>[^/]+)=(?P<name>.+)$")


class Validator(Protocol):
    def part(self, name: str, part: Literal["vendor", "class"]) -> None: ...
    def device_name(self, name: str) -> None: ...


class QualifiedDeviceName(Struct, array_like=True):
    vendor: str
    class_: str
    name: str

    @classmethod
    def from_str(cls, device: str, validator: Validator):
        validate = validator
        match = DEVICE_RE.match(device)

        if not match:
            raise DeviceNameError(device)

        vendor = match.group("vendor")
        validate.part(vendor, "vendor")

        class_name = match.group("class")
        validate.part(class_name, "class")

        name = match.group("name")
        validate.device_name(name)

        return cls(vendor, class_name, name)


class RegexValidator:
    @staticmethod
    def part(name: str, part: Literal["vendor", "class"]):
        match = re.match(r"^[a-zA-Z][a-zA-Z0-9_-.]+[a-zA-Z0-9]$", name)
        if not match:
            raise DeviceNameError(name, part=part)

    @staticmethod
    def device_name(name: str):
        match = re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_-.:]+[a-zA-Z0-9]$", name)
        if not match:
            raise DeviceNameError(name)


class DebugValidator:
    @staticmethod
    def part(name: str, part: Literal["vendor", "class"]):
        if not name:
            raise DeviceNameError("", "empty", part)
        if not name[0].isalpha():
            raise DeviceNameError(name, "should start with a letter", part)

        if len(name) > 1:
            for c in name[1:-1]:
                if not (c.isalnum() or c in {"_", "-", "."}):
                    raise DeviceNameError(name, f"invalid character {c}", part)

            if not name[-1].isalnum():
                raise DeviceNameError(name, "should end with a letter or digit", part)
        elif not name[0].isalnum():
            raise DeviceNameError(name, "should end with a letter or digit", part)

    @staticmethod
    def device_name(name: str):
        if not name:
            raise DeviceNameError(name, "empty")
        if not name[0].isalnum():
            raise DeviceNameError(name, "should start with a letter or digit")

        if len(name) > 1:
            for c in name[1:-1]:
                if not (c.isalnum() or c in {"_", "-", ".", ":"}):
                    raise DeviceNameError(name, f"invalid character {c}")

            if not name[-1].isalnum():
                raise DeviceNameError(name, "should end with a letter or digit")
