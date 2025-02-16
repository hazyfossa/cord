from collections.abc import AsyncIterator
from typing import Annotated
from httpx import URL, AsyncClient
from msgspec import Meta
from pyoci.image.manifest import Manifest
from pyoci.image.well_known import (
    OciMediaType,
)  # TODO: get that from ImageManifest once we figure out typing for mediaType
from msgspec import json

Name = Annotated[
    str,
    # Note: this annotation is not used at runtime currently, it's only for documentation
    Meta(
        pattern=r"[a-z0-9]+((\.|_|__|-+)[a-z0-9]+)*(\/[a-z0-9]+((\.|_|__|-+)[a-z0-9]+)*)*"
    ),
]

Reference = Annotated[str, Meta(pattern=r"[a-zA-Z0-9_][a-zA-Z0-9._-]{0,127}")]


# TODO: support checking existence with HEAD


class RegistryClient:
    def __init__(self, url: str):
        self.api = AsyncClient(base_url=URL(url).join("v2"))

    async def get_manifest(self, repository: str, reference: Reference) -> Manifest:
        headers = {"Accept": OciMediaType.image_manifest}
        response = await self.api.get(
            f"{repository}/manifests/{reference}", headers=headers
        )

        # TODO: verify that mediaType matches Content-Type
        return json.decode(response.read())

    # TODO: verify digest
    async def get_blob(
        self, repository: str, digest: str, chunk_size: int | None = None
    ) -> AsyncIterator[bytes]:
        response = await self.api.get(f"{repository}/blobs/{digest}")

        if response.status_code == 404:
            raise FileNotFoundError(f"Blob {digest} not found")

        return response.aiter_bytes(chunk_size=chunk_size)
