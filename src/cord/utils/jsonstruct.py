from collections.abc import Buffer

from msgspec import json


class JsonStruct:
    @classmethod
    def loads(cls, data: Buffer | str):
        return json.decode(data, type=cls)

    def dumps(self) -> bytes:
        return json.encode(self)
