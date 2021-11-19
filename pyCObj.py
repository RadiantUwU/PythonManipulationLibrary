import ctypes
from typing import Dict, Type, Any, Tuple

Py_ssize_t = ctypes.c_int64 if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_int32


class PyObject(ctypes.Structure):
    def incref(self):
        self.ob_refcnt += 1

    def decref(self):
        self.ob_refcnt -= 1


class PyFile(ctypes.Structure):
    ...


PyObject_p = ctypes.py_object
Inquiry_p = ctypes.CFUNCTYPE(ctypes.c_int, PyObject_p)
UnaryFunc_p = ctypes.CFUNCTYPE(PyObject_p, PyObject_p)
BinaryFunc_p = ctypes.CFUNCTYPE(PyObject_p, PyObject_p, PyObject_p)
TernaryFunc_p = ctypes.CFUNCTYPE(PyObject_p, PyObject_p, PyObject_p, PyObject_p)
LenFunc_p = ctypes.CFUNCTYPE(Py_ssize_t, PyObject_p)
SSizeArgFunc_p = ctypes.CFUNCTYPE(PyObject_p, PyObject_p, Py_ssize_t)
SSizeObjArgProc_p = ctypes.CFUNCTYPE(ctypes.c_int, PyObject_p, Py_ssize_t, PyObject_p)
ObjObjProc_p = ctypes.CFUNCTYPE(ctypes.c_int, PyObject_p, PyObject_p)
visitproc_p = ctypes.CFUNCTYPE(PyObject_p, ctypes.c_void_p)

FILE_p = ctypes.POINTER(PyFile)


def get_not_implemented():
    namespace = {}
    name = "_Py_NotImplemented"
    # noinspection PyProtectedMember
    not_implemented = ctypes.cast(
        ctypes.pythonapi._Py_NotImplementedStruct, ctypes.py_object)

    ctypes.pythonapi.PyDict_SetItem(
        ctypes.py_object(namespace),
        ctypes.py_object(name),
        not_implemented
    )
    return namespace[name]


NotImplementedRet = get_not_implemented()


class PyNumberMethods(ctypes.Structure):
    _fields_ = [
        ('nb_add', BinaryFunc_p),
        ('nb_subtract', BinaryFunc_p),
        ('nb_multiply', BinaryFunc_p),
        ('nb_remainder', BinaryFunc_p),
        ('nb_divmod', BinaryFunc_p),
        ('nb_power', BinaryFunc_p),
        ('nb_negative', UnaryFunc_p),
        ('nb_positive', UnaryFunc_p),
        ('nb_absolute', UnaryFunc_p),
        ('nb_bool', Inquiry_p),
        ('nb_invert', UnaryFunc_p),
        ('nb_lshift', BinaryFunc_p),
        ('nb_rshift', BinaryFunc_p),
        ('nb_and', BinaryFunc_p),
        ('nb_xor', BinaryFunc_p),
        ('nb_or', BinaryFunc_p),
        ('nb_int', UnaryFunc_p),
        ('nb_reserved', ctypes.c_void_p),
        ('nb_float', UnaryFunc_p),

        ('nb_inplace_add', BinaryFunc_p),
        ('nb_inplace_subtract', BinaryFunc_p),
        ('nb_inplace_multiply', BinaryFunc_p),
        ('nb_inplace_remainder', BinaryFunc_p),
        ('nb_inplace_power', TernaryFunc_p),
        ('nb_inplace_lshift', BinaryFunc_p),
        ('nb_inplace_rshift', BinaryFunc_p),
        ('nb_inplace_and', BinaryFunc_p),
        ('nb_inplace_xor', BinaryFunc_p),
        ('nb_inplace_or', BinaryFunc_p),

        ('nb_floor_divide', BinaryFunc_p),
        ('nb_true_divide', BinaryFunc_p),
        ('nb_inplace_floor_divide', BinaryFunc_p),
        ('nb_inplace_true_divide', BinaryFunc_p),

        ('nb_index', BinaryFunc_p),

        ('nb_matrix_multiply', BinaryFunc_p),
        ('nb_inplace_matrix_multiply', BinaryFunc_p),
    ]


class PySequenceMethods(ctypes.Structure):
    _fields_ = [
        ('sq_length', LenFunc_p),
        ('sq_concat', BinaryFunc_p),
        ('sq_repeat', SSizeArgFunc_p),
        ('sq_item', SSizeArgFunc_p),
        ('was_sq_slice', ctypes.c_void_p),
        ('sq_ass_item', SSizeObjArgProc_p),
        ('was_sq_ass_slice', ctypes.c_void_p),
        ('sq_contains', ObjObjProc_p),
        ('sq_inplace_concat', BinaryFunc_p),
        ('sq_inplace_repeat', SSizeArgFunc_p),
    ]


class PyMappingMethods(ctypes.Structure):
    ...


class PyTypeObject(ctypes.Structure):
    pass


class PyAsyncMethods(ctypes.Structure):
    ...


class PyBufferProcs(ctypes.Structure):
    ...  # not made


# noinspection PyPep8Naming
class Py_buffer(ctypes.Structure):
    _fields_ = [
        ('buf', ctypes.c_void_p),
        ('obj', ctypes.c_void_p),
        ('len', Py_ssize_t),
        ('readonly', ctypes.c_int),
        ('itemsize', Py_ssize_t),
        ('format', ctypes.c_char_p),
        ('ndim', ctypes.c_int),
        ('shape', ctypes.POINTER(Py_ssize_t)),
        ('strides', ctypes.POINTER(Py_ssize_t)),
        ('suboffsets', ctypes.POINTER(Py_ssize_t)),
        ('internal', ctypes.c_void_p)
    ]


PyObject._fields_ = [
    ('ob_refcnt', Py_ssize_t),
    ('ob_type', ctypes.POINTER(PyTypeObject))
    # ...
]

PyTypeObject._fields_ = [
    # varhead
    ('ob_base', PyObject),
    ('ob_size', Py_ssize_t),
    # declare stuff
    ('tp_name', ctypes.c_char_p),
    ('tp_basicsize', Py_ssize_t),
    ('tp_itemsize', Py_ssize_t),
    ('tp_dealloc', ctypes.CFUNCTYPE(None, PyObject_p)),
    ('printfunc', ctypes.CFUNCTYPE(ctypes.c_int, PyObject_p, FILE_p, ctypes.c_int)),
    ('getattrfunc', ctypes.CFUNCTYPE(PyObject_p, PyObject_p, ctypes.c_char_p)),
    ('setattrfunc', ctypes.CFUNCTYPE(ctypes.c_int, PyObject_p, ctypes.c_char_p, PyObject_p)),
    ('tp_as_async', ctypes.CFUNCTYPE(PyAsyncMethods)),
    ('tp_repr', UnaryFunc_p),
    ('tp_as_number', ctypes.POINTER(PyNumberMethods)),
    ('tp_as_sequence', ctypes.POINTER(PySequenceMethods)),
    ('tp_as_mapping', ctypes.POINTER(PyMappingMethods)),
    ('tp_hash', ctypes.CFUNCTYPE(ctypes.c_int64, PyObject_p)),
    ('tp_call', TernaryFunc_p),
    ('tp_str', UnaryFunc_p),
    ('tp_getattro', UnaryFunc_p),
    ('tp_setattro', BinaryFunc_p),
    ('tp_as_buffer', PyBufferProcs),
    ('tp_flags', ctypes.c_ulong),
    ('tp_doc', ctypes.c_char_p),
    ('tp_traverse', ctypes.CFUNCTYPE(PyObject_p, visitproc_p, ctypes.c_void_p)),
    ('tp_clear', Inquiry_p),
    ('tp_richcompare', ctypes.CFUNCTYPE(PyObject_p, PyObject_p, ctypes.c_int)),
    ('tp_weaklistoffset', Py_ssize_t),
    ('tp_iter', UnaryFunc_p),
    ('iternextfunc', UnaryFunc_p),
    ('tp_methods', ctypes.c_void_p),  # lolol define it urself
    ('tp_members', ctypes.c_void_p),  # and this
    ('tp_getset', ctypes.c_void_p),  # and this
    ('tp_base', ctypes.POINTER(PyTypeObject)),
    ('tp_dict', PyObject_p),
    ('tp_descr_get', TernaryFunc_p),
    ('tp_descr_set', TernaryFunc_p),
    ('tp_dictoffset', Py_ssize_t),
    ('tp_init', ctypes.CFUNCTYPE(ctypes.c_int, PyObject_p, PyObject_p, PyObject_p)),
    ('tp_alloc', ctypes.CFUNCTYPE(PyObject_p, ctypes.POINTER(PyTypeObject), Py_ssize_t)),
    ('tp_new', TernaryFunc_p),
    ('tp_free', ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
    ('tp_is_gc', Inquiry_p),
    ('tp_bases', PyObject_p),
    ('tp_mro', PyObject_p),
    ('tp_cache', PyObject_p),
    ('tp_subclasses', PyObject_p),
    ('tp_weaklist', PyObject_p),
    ('tp_del', ctypes.CFUNCTYPE(None, PyObject_p)),
    ('tp_version_tag', ctypes.c_uint),
    ('tp_finalize', ctypes.CFUNCTYPE(None, PyObject_p)),
    ('tp_bases', PyObject_p),
    ('tp_vectorcall', ctypes.c_void_p)  # lmao i wont define it uwu
    # more can be defined
]


class PyTupleObject:
    _class_instances: Dict[int, Type[ctypes.Structure]] = {}

    def __new__(cls, tup: Tuple[Any, ...]):
        if len(tup) in cls._class_instances.keys():
            return cls._class_instances[len(tup)].from_address(id(tup))
        else:
            class PyTupleObject(ctypes.Structure):
                _len = len(tup)
                _fields_ = [
                    ('ob_refcnt', Py_ssize_t),
                    ('ob_type', ctypes.POINTER(PyTypeObject)),
                    ('ob_size', ctypes.c_int),
                    ('ob_item', PyObject_p * _len)
                ]
            cls._class_instances[len(tup)] = PyTupleObject
            return PyTupleObject.from_address(id(tup))


# class PyNamedTupleObject:
#     _class_instances: Dict[int, Type[ctypes.Structure]] = {}
#
#     def __new__(cls, tup: NamedTuple[Any, ...]):
#         if len(tup) in cls._class_instances.keys():
#             return cls._class_instances[len(tup)].from_address(id(tup))
#         else:
#             class NamedTupleItems(ctypes.Structure):
#                 _len = len(tup)
#                 _fields_ = [
#                     ('ob_refcnt', Py_ssize_t),
#                     ('ob_type', ctypes.POINTER(PyTypeObject)),
#                     ('ob_size', ctypes.c_int),
#                     ('ob_item', PyObject_p * _len)
#                 ]
#             class PyNamedTupleObject(ctypes.Structure):
#                 _len = len(tup)
#                 _fields_ = [
#                     ('ob_refcnt', Py_ssize_t),
#                     ('ob_type', ctypes.POINTER(PyTypeObject)),
#                     ('ob_size', ctypes.c_int),
#                     ('ob_item', PyObject_p * _len)
#                 ]
#             cls._class_instances[len(tup)] = PyNamedTupleObject
#             return PyNamedTupleObject.from_address(id(tup))

pythonapi = ctypes.pythonapi
