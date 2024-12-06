from pyoci.spec import Container
from msgspec import json

c = Container("1.2.0")
print(json.encode(c))
