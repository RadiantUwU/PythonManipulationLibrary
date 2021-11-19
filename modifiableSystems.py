import copy
import ctypes
from types import FunctionType
from typing import Callable, List, Tuple, Dict, Any, overload

from nullObj import null
from pyCObj import PyTypeObject, PyObject, PyObject_p, pythonapi

split_type = (lambda cls: (cls.__name__, cls.__bases__, PyTypeObject.from_address(id(cls)).tp_dict))


class ModifiableFunction:
    class wrapFunc:
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            self.func(*(list(args)[1:]), **kwargs)

    def __init__(self, baseFunction: Callable = None):
        if baseFunction is not None:
            self.function_list: List[Callable] = [baseFunction]
        else:
            self.function_list: List[Callable] = []

    def __call__(self, *args, **kwargs):
        load_locals = (lambda locals_dict, locals_: [locals_dict.__setitem__(k, v) for k, v in locals_.items()])

        def runSuperFunction(*args, **kwargs):
            nonlocal i
            if i != 0:
                i -= 1
                return self.function_list[i](
                    {'i': i, 'runSuperFunction': runSuperFunction, 'self': self, 'load_locals': load_locals}, *args,
                    **kwargs)
            return null

        i = len(self.function_list) - 1
        if i > -1:
            return self.function_list[i](
                {'i': i, 'runSuperFunction': runSuperFunction, 'self': self, 'load_locals': load_locals}, *args,
                **kwargs)

    def addFunction(self, function: Callable):
        self.function_list.append(function)
        return self

    def clear(self):
        self.function_list.clear()


class ModifiableClass(type):
    @staticmethod
    def setClass(obj, klass: type):
        PyObject.from_address(id(obj)).ob_type = ctypes.pointer(PyTypeObject.from_address(id(klass)))

    def addClassHP(cls, hp_cls: type):
        py_type = PyTypeObject.from_address(id(cls))
        name, bases, old_dict = split_type(cls)
        cls_copy = ModifiableClass.__new__(ModifiableClass, name, bases, copy.copy(old_dict))
        name, bases, dict = split_type(hp_cls)
        bases = list(bases)
        bases.append(cls_copy)
        try:
            bases.remove(object)
        except ValueError:
            pass
        dict = dict.copy()
        for k, v in old_dict.items():
            if k == "__name__":
                continue
            dict.setdefault(k, v)
        new_cls = ModifiableClass.__new__(ModifiableClass, name, tuple(bases), copy.copy(dict))
        py_type.tp_bases = new_cls.__bases__
        py_type.tp_mro = new_cls.__mro__
        py_type.tp_dict = dict
        pythonapi.PyType_Modified(PyObject_p(cls))

    def addBase(cls, base: type, position: int = -1):
        py_type = PyTypeObject.from_address(id(cls))
        name, bases, dict = split_type(cls)
        bases = list(bases)
        bases.insert(position, base)
        try:
            bases.remove(object)
        except ValueError:
            pass
        bases = tuple(bases)
        new_cls = ModifiableClass.__new__(ModifiableClass, name, bases, copy.copy(dict))
        py_type.tp_mro = new_cls.__mro__
        py_type.tp_bases = new_cls.__bases__
        pythonapi.PyType_Modified(PyObject_p(cls))

    def setBases(cls, bases: Tuple[type]):
        py_type = PyTypeObject.from_address(id(cls))
        name, _, dict = split_type(cls)
        new_cls = ModifiableClass.__new__(ModifiableClass, name, bases, copy.copy(dict))
        py_type.tp_mro = new_cls.__mro__
        py_type.tp_bases = new_cls.__bases__
        pythonapi.PyType_Modified(PyObject_p(cls))

    @property
    def __dict__(cls) -> Dict[str, Any]:
        return PyTypeObject.from_address(id(cls)).tp_dict

    @__dict__.setter
    def __dict__(cls, dict_object: Dict[str, Any]):
        PyTypeObject.from_address(id(cls)).tp_dict = dict_object
        pythonapi.PyType_Modified(PyObject_p(cls))

    def __copy__(cls):
        return type(cls).copy(cls)

    def copy(cls):
        name, bases, dict_obj = split_type(cls)
        return type(cls).__new__(type(cls), name, bases, dict_obj.copy())


class Singleton:
    __instance__ = null

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is null:
            inst = super().__new__(cls, *args, **kwargs)
            cls.__instance__ = inst
            return inst
        return cls.__instance__

    def __del__(self):
        type(self).__instance__ = null


class UndeletableSingleton(Singleton):
    __instance__ = null

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is null:
            inst = super().__new__(cls, *args, **kwargs)
            cls.__instance__ = inst
            PyObject.from_address(id(inst)).incref()
            return inst
        return cls.__instance__


class AttributableMethod:
    def __init__(self, func, **kwargs):
        self._func = func
        self.__code__ = func.__code__
        for k, v in kwargs.items():
            super().__setattr__(k, v)

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


# noinspection SpellCheckingInspection
@overload
def attributablemethod(**kwargs) -> Callable[[FunctionType], AttributableMethod]:
    pass


# noinspection SpellCheckingInspection
@overload
def attributablemethod(func) -> AttributableMethod:
    pass


# noinspection SpellCheckingInspection
def attributablemethod(func=null, **kwargs):
    if func is null:
        def wrapper(func):
            return AttributableMethod(func, **kwargs)
        return wrapper
    else:
        return AttributableMethod(func)
