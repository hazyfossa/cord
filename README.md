# pyoci

[![image](https://img.shields.io/pypi/v/pyoci.svg)](https://pypi.python.org/pypi/pyoci)
[![image](https://img.shields.io/pypi/l/pyoci.svg)](https://pypi.python.org/pypi/pyoci)
[![image](https://img.shields.io/pypi/pyversions/pyoci.svg)](https://pypi.python.org/pypi/pyoci)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**What**: A library to define OCI [Runtime](https://github.com/opencontainers/runtime-spec) and [Image](https://github.com/opencontainers/image-spec) specification compliant container instances.

**When**: When you need to run or modify a container at the lowest level, without docker, containerd or podman.

**Why**: The full OCI specifications can be quite large to read, and even trickier to implement. This library saves you all the json-wrangling and validation, without abstracting any features away.

# notes

* This project has nothing to do with [PyOCI](https://github.com/AllexVeldman/pyoci) - the oci registry proxy for python packages. The current name of this library will most likely be changed in the future.
* This library is heavily WIP, so there are no guarantees about API stability until a 1.x release.
* This is a low-level library. If you want to simply run a container, without configuring all the inner workings, i'd suggest [docker-py](https://github.com/docker/docker-py).
