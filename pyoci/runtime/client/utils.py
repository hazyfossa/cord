# - default with encode=False is only for documentation
# (i.e. showing default values within a container runtime)
# - default with encode=True is a regular python default
def default(value, encode=False):
    if encode:
        return value

    return None
