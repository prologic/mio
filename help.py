def foo(a, b):
    """Calculate a + b"""

    return a + b


def bar(a, b):
    return a + b


class Foo(object):
    """Foo"""

    def foo(self, a, b):
        """Calculate a + b"""

        return a + b


class Bar(object):

    def bar(self, a, b):
        return a + b
