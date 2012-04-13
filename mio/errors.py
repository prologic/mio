class Error(Exception):
    """Base Class for Mio Errors"""


class ArgsError(Error):
    """Args Error"""

    def __init__(self, nargs, method):
        self.nargs = nargs
        self.method = method

    def __str__(self):
        actual = self.nargs
        method = self.method
        expected = method.nargs[0]

        if len(method.nargs) == 1:
            plural = "exactly"
        else:
            plural = "at least"

        return "Args Error: %s takes %s %d arguments(s), %d provided" % (
                method.name, plural, expected, actual)


class SlotError(Error):
    """Slot Error"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Slot Error: %s" % self.name
