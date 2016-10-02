def singleton(cls):
    _instances = {}

    def wrapper(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        print _instances
        return _instances[cls]

    return wrapper


@singleton
class Foo(object):
    def __init__(self, a=0):
        self.a = a


foo1 = Foo(1)
foo2 = Foo(2)
print foo1.a  # Out: 1
print foo2.a  # Out: 1
print id(foo1) == id(foo2)
