class Error(Exception):
    """Base Class for Mio Errors"""


class ArgsError(Error):
    """Args Error"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Args Error: expected %d got %d" % (self.x, self.y)


class SlotError(Error):
    """Slot Error"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Slot Error: %s" % self.name
