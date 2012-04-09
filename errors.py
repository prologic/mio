class Error(Exception):
    """Base Class for Mio Errors"""


class SlotError(Error):
    """Slot Error"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Slot Error: %s" % self.name
