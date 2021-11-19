from pyCObj import PyObject_p

e = 0


class NullType:
    def __new__(cls, *args, **kwargs):
        global e
        if e != 0:
            return PyObject_p.from_address(e).value
        x = super().__new__(cls)
        e = id(x)
        return x


class NullClass:
    def __getattr__(self, item):
        return NullClass()

    def __setattr__(self, key, value):
        pass

    def __getitem__(self, item):
        return NullClass()

    def __setitem__(self, key, value):
        pass

    def __int__(self):
        return 0

    def __index__(self):
        return 0

    def __float__(self):
        return 0.0

    def __call__(self, *args, **kwargs):
        pass


null = NullType()
__all__ = [null, NullClass]
