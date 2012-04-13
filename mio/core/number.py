from mio.object import method, Object

class Number(Object):

    # General Arithmetic

    @method()
    def __add__(self, other):
        return self.clone(self.value.__add__(other.value))

    @method()
    def __sub__(self, other):
        return self.clone(self.value.__sub__(other.value))

    @method()
    def __mul__(self, other):
        return self.clone(self.value.__mul__(other.value))

    @method()
    def __div__(self, other):
        return self.clone(self.value.__div__(other.value))

    # Type Conversion

    @method()
    def __int__(self):
        return self.clone(self.value.__int__())

    @method()
    def __float__(self):
        return self.clone(self.value.__float__())
