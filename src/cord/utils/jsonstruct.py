from msgspec import json


from collections.abc import Buffer


class SimpleJsonMixin:
    @classmethod
    def loads(cls, data: Buffer | str):
        return json.decode(data, type=cls)

    def dumps(self) -> bytes:
        return json.encode(self)
