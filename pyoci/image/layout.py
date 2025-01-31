from pathlib import Path
from typing import Iterable, Literal
from pyoci.common import Struct
from pyoci.image.manifest import Index
from pyoci.image.descriptor import Descriptor
from msgspec import json, ValidationError


# TODO: Allow accessing undefined fields, or consider unstructured decoding
class LayoutFile(Struct):
    imageLayoutVersion: Literal["1.0.0"] = "1.0.0"


class LayoutError(Exception):
    def __init__(self, path: Path, message: str) -> None:
        self.message = f"{path} is not a valid OCI layout: {message}"


def read_layout_part[T](layout_root: Path, part: str, type: T) -> T:
    path = layout_root / part

    if not path.exists():
        raise LayoutError(layout_root, f"{part} file not found")

    try:
        return json.decode(path.read_bytes(), type=type)
    except ValidationError as e:
        raise LayoutError(layout_root, f"{part} file is invalid: {e}")


class OCILayout:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

        self.marker = read_layout_part(self.path, "oci-layout", LayoutFile)
        self.index = read_layout_part(self.path, "index.json", Index)

    def upload_blob(self, descriptor: Descriptor, blob: Iterable[bytes]) -> None: ...
