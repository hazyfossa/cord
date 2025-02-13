from pathlib import Path
from typing import IO, BinaryIO, Literal

from msgspec import ValidationError, json

from pyoci.common import Struct
from pyoci.image.descriptor import Descriptor, ManifestDescriptor
from pyoci.image.digest import Digest
from pyoci.image.manifest import Index


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
        self.blob_root = self.path / "blobs"

        self.meta = read_layout_part(self.path, "oci-layout", LayoutFile)
        self.index = read_layout_part(self.path, "index.json", Index)

        if not self.blob_root.exists():
            raise LayoutError(self.path, "'blobs' directory not found")

        # TODO: check if extra memory usage is worth the speedup
        # Alternative would be to do (self.blob_root / alg).mkdir(exist_ok=True) on each blob upload
        self.algs_used = set()

    @classmethod
    def make(cls, path: Path | str, exists_ok: bool = False) -> None:
        path = Path(path)
        marker_file = path / "oci-layout"

        if marker_file.exists():
            if not exists_ok:
                raise ValueError(f"{path} is already an OCI layout")

            return

        empty_index = Index(manifests=[])
        (path / "oci-layout").write_bytes(json.encode(LayoutFile()))
        (path / "index.json").write_bytes(json.encode(empty_index))
        (path / "blobs").mkdir()

    def has_blob(self, digest: Digest) -> bool:
        path = self.blob_root / digest.algorithm / digest.value
        return path.exists()

    def read_blob(self, digest: Digest) -> IO[bytes]:
        path = self.blob_root / digest.algorithm / digest.value
        return path.open("rb")  # type: ignore # implicit cast

    def write_blob(self, digest: Digest, blob: BinaryIO) -> None:
        path = self.blob_root / digest.algorithm

        if digest.algorithm not in self.algs_used:
            path.mkdir()
            self.algs_used.add(digest.algorithm)

        # TODO: optimize memory usage
        path.write_bytes(blob.read())
