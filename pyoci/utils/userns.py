# Code adapted from https://github.com/moby/sys/blob/main/userns/userns_linux.go

UID_MAP_FILE = "/proc/self/uid_map"


def running_in_user_ns() -> bool:
    try:
        with open(UID_MAP_FILE, "r") as file:
            line = file.readline().strip()
            return uid_map_in_user_ns(line)
    except FileNotFoundError:
        # This kernel-provided file only exists if user namespaces are supported.
        return False


def uid_map_in_user_ns(uid_map: str) -> bool:
    if uid_map == "":
        # File exists but is empty (the initial state when userns is created,
        # see user_namespaces(7)).
        return True

    try:
        a, b, c = map(int, uid_map.split())
    except ValueError:
        # Assume we are in a regular, non-user namespace.
        return False

    # As per user_namespaces(7), /proc/self/uid_map of
    # the initial user namespace shows 0 0 4294967295.
    init_ns = a == 0 and b == 0 and c == 4294967295
    return not init_ns
