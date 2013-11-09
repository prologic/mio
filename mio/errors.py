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


class TypeError(Error):
    """TypeError"""


class UserError(Error):
    """UserError"""
