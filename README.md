# pyoci

[![image](https://img.shields.io/pypi/v/pyoci.svg)](https://pypi.python.org/pypi/pyoci)
[![image](https://img.shields.io/pypi/l/pyoci.svg)](https://pypi.python.org/pypi/pyoci)
[![image](https://img.shields.io/pypi/pyversions/pyoci.svg)](https://pypi.python.org/pypi/pyoci)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**What**: A library to define OCI [Runtime](https://github.com/opencontainers/runtime-spec) and [Image](https://github.com/opencontainers/image-spec) specification compliant container instances.

**When**: When you need to run or modify a container at the lowest level, without containerd or docker/podman.

**Why**: The full OCI specifications can be quite large to read, and even trickier to implement. This library saves you all the json-wrangling and validation, without abstracting any features away.

**How**: Under the hood, everything here is a msgpack Struct. These structs were generated from the original json-schema with help of [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) and then manually refactored by me.

#
**Pros**:
- Full control over the container.
- Compatible with many runtimes.
- Very lightweight[^1].

**Cons**:
- Requires low-level knowledge of how a container is constructed.
- Isn't well tested (for now).

#

This is a low-level library. If you want to simply run a container, without configuring all the inner workings, i'd suggest [docker-py](https://github.com/docker/docker-py).

This library is runtime-agnostic, so it doesn't provide a way to actually run the container. You'll need to pass the definition to an appropriate runtime yourself.

Also, I want to say a huge thanks to koxudaxi and other contributors for the awesome code generator!

[^1]: Pyoci should be very fast and memory/resource efficent thanks to use of msgspec. The performance of actually running the container will depend on your provided runtime.