from io import TextIOWrapper
from pathlib import Path

from pyoci.runtime.client import Runc
from pyoci.runtime.config.templates.default import ContainerConfig, Process

# The id for your new container, must be unique across the system
ID = "test"

# While support for OCI images is in development, you'll need to provide the container rootfs yourself.
# This assumes ./test/container/rootfs/ is an unpacked rootfs suitable for the container.
BUNDLE = Path("./test/container/")

# Define all required parameters for the container
process = Process(args=["/bin/hostname"], terminal=False)
c = ContainerConfig(process, hostname="pyoci-test-container")

c.write_bundle(BUNDLE)

runc = Runc()

# .create() returns the container's IO. It is empty until container is started.
io = runc.create(ID, bundle=BUNDLE)

runc.start(ID)

# Print the container's stdout
stdout = TextIOWrapper(io.stdout)
for line in stdout.readlines():
    print(line, end="")

runc.delete(ID)
