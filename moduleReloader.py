import gc
import inspect
from collections.abc import MutableSequence, MutableSet, MutableMapping, Sequence
from types import FrameType
from typing import Any, List

from pyCObj import PyTupleObject


def map_index(map_obj: Mapping, obj: Any):
    for k, v in map_obj.items():
        if v is obj:
            return k
    raise IndexError("object does not exist in dictionary.")


def tuple_replace(tup, from_, to):
    x = PyTupleObject(tup)
    for k, v in enumerate(x.ob_item):
        if v is from_:
            x.ob_item[k] = to


def replace_all(from_: Any, to: Any):
    references: List[Sequence | FrameType] = gc.get_referents(from_)
    for ref in references:
        if inspect.isframe(ref):  # if its a frame but not this frame replace it
            if ref is not inspect.currentframe():
                while from_ in ref.f_locals.values():
                    ref.f_locals[map_index(ref.f_locals, from_)] = to
                while from_ in ref.f_globals.values():
                    ref.f_globals[map_index(ref.f_globals, from_)] = to
        elif isinstance(ref, MutableSequence) or isinstance(ref, MutableMapping) or isinstance(ref, MutableSet):
            if isinstance(ref, MutableSequence):
                while from_ in ref:
                    ref[ref.index(from_)] = to
            elif isinstance(ref, MutableMapping):
                while from_ in ref.values():
                    ref[map_index(ref, from_)] = to
            else:
                while from_ in ref:
                    ref.remove(from_)
                    ref.add(to)
        elif isinstance(ref, tuple):
            tuple_replace(ref, from_, to)


def reload_module(name: str):
    placeholder = object()
    replace_all(__import__(name), placeholder)
    replace_all(placeholder, __import__(name))
