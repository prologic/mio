class Error(Exception):
    """Error"""

    def __init__(self, *args):
        super(Error, self).__init__(*args)

        self.stack = []


class AttributeError(Error):
    """AttributeError"""


class TypeError(Error):
    """TypeError"""


class ImportError(Error):
    """ImportError"""


class UserError(Error):
    """UserError"""
