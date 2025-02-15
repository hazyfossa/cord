from pathlib import Path
from typing import Literal

from msgspec import ValidationError, json

from pyoci.common import Struct, Unset
from pyoci.image.digest import DEFAULT_ALGORITHM, Digest
from pyoci.image.manifest import Index, Manifest, ManifestDescriptor
from pyoci.image.well_known import ImageAnnotation


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

        self.tags = self._populate_tags()

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

    def blob(self, digest: Digest) -> Path:
        # TODO: return a modified object with a .create method, so new_blob is redundant
        return self.blob_root / digest.algorithm / digest.value

    def new_blob(self, digest: Digest, overwrite_ok: bool = False) -> Path:
        alg_path = self.blob_root / digest.algorithm

        if digest.algorithm not in self.algs_used:
            alg_path.mkdir()
            self.algs_used.add(digest.algorithm)

        return alg_path / digest.value

    def read_manifest(self, tag: str) -> Manifest:
        descriptor = self.tags[tag]
        blob = self.blob(Digest.from_str(descriptor.digest)).read_bytes()
        return json.decode(blob, type=Manifest)

    def write_struct(
        self, struct: Struct, digest_algorithm: str = DEFAULT_ALGORITHM
    ) -> None:
        content = json.encode(struct)
        digest = Digest.from_bytes(content, digest_algorithm)
        blob = self.new_blob(digest)

        blob.write_bytes(content)

    def _populate_tags(self) -> dict[str, ManifestDescriptor]:
        manifests_by_tag = {}

        for manifest_descriptor in self.index.manifests:
            if isinstance(manifest_descriptor.annotations, Unset):
                continue

            tag: str | None = manifest_descriptor.annotations.get(
                ImageAnnotation.ref_name
            )

            if tag is None:
                continue

            manifests_by_tag[tag] = manifest_descriptor

        return manifests_by_tag
