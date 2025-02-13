from pyoci.runtime.config.templates.default import ContainerConfig, Process
from pyoci.runtime.client import Runc
from io import TextIOWrapper

# The id for your new container, must be unique across the system
ID = "test"

# While support for OCI images is in development, you'll need to provide the container rootfs yourself.
# This assumest ./test/container/rootfs/ is an unpacked rootfs suitable for the container.
BUNDLE = "./test/container/"

# Define all required parameters for the container
process = Process(args=["/bin/hostname"], terminal=False)
c = ContainerConfig(process, hostname="pyoci-test-container")

# Write the config. The filename should always be config.json per the specification.
with open("./test/container/config.json", "wb") as f:
    f.write(c.dumps())

runc = Runc("/usr/sbin/runc")

# .create() returns the container's IO. It is empty until container is started.
io = runc.create(ID, bundle=BUNDLE)

runc.start(ID)

# Print the container's stdout
stdout = TextIOWrapper(io.stdout)
for line in stdout.readlines():
    print(line, end="")

# Delete the container after you're finished
runc.delete(ID)
