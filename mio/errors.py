class Error(Exception):
    """Error"""

    def __init__(self, *args):
        super(Error, self).__init__(*args)

        self.stack = []


class AttributeError(Error):
    """AttributeError"""


class ImportError(Error):
    """ImportError"""


class IndexError(Error):
    """IndexError"""


class KeyError(Error):
    """KeyError"""


class TypeError(Error):
    """TypeError"""


class StopIteration(Error):
    """StopIteration"""


class UserError(Error):
    """UserError"""
