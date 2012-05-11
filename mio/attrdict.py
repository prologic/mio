class AttrDict(dict):

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        self.__dict__.update(zip(items, items))

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__,
                super(AttrDict, self).__repr__())

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(AttrDict, self).__getitem__(name)

    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        return AttrDict(self)

    def update(self, other):
        super(AttrDict, self).update(other)
        return self
