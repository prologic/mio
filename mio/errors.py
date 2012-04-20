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

        if len(method.nargs) == 1:
            plural = "exactly"
            expected = method.nargs[0]
        else:
            if len(actual) > method.nargs[1]:
                plural = "at most"
                expected = method.nargs[1]
            else:
                plural = "at least"
                expected = method.nargs[0]

        return "Args Error: %s takes %s %d arguments(s), %d provided" % (
                method.name, plural, expected, actual)


class SlotError(Error):
    """Slot Error"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Slot Error: %s" % self.name


class TypeError(Error):
    """Type Error"""

    def __init__(self, method, expected, actual):
        self.method = method
        self.expected = expected
        self.actual = actual


    def __str__(self):
        return "Type Error: expected %s in %s got %s" % (self.expected,
                self.method.name, self.actual)
