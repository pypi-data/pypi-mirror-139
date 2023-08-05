# coding=utf-8
import itertools
from collections.abc import MutableMapping
from typing import Mapping


class AttrDict(MutableMapping):
    """@DynamicAttrs"""

    # attributes that are included in the iteration (generally used for a property of a subclass)
    _special_attributes = tuple()

    def __setitem__(self, k, v):
        self._d[k] = v

    def __delitem__(self, v) -> None:
        del self._d[v]

    def __len__(self) -> int:
        return len(self._d)

    def __iter__(self):
        if self._special_attributes:
            return itertools.chain(self._d.__iter__(), self._special_attributes)
        else:
            return self._d.__iter__()

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    # def __iter__(self):
    #     for k in self._d.keys():
    #         yield k
    #
    # def __len__(self) -> int:
    #     return self._.__len__()

    def __init__(self, *args, _parent_key=None, **kwargs):
        super().__init__()
        self._parent_key = _parent_key
        self._d = dict(*args, **kwargs)

    def __getattr__(self, k):

        if not k.startswith("_") and k in self._d:
            return self.__getitem__(k)
        return getattr(super(), k)
        # return super().__getattribute__(k)

    def __getitem__(self, k):
        if k in self._special_attributes:
            v = getattr(self, k)
        else:
            v = self._d[k]
        if isinstance(v, Mapping):
            return AttrDict(v)
        return v

    def __repr__(self):
        return f"{self.__class__.__name__}({self._d})"

    def items(self, flat_key=False):
        for k, v in self._d.items():
            if flat_key and self._parent_key is not None:
                k = f"{self._parent_key}.{k}"
            if isinstance(v, Mapping):
                yield k, AttrDict(v)
            else:
                yield k, v

    def items_flat(self):
        for k, v in self.items(flat_key=True):
            if isinstance(v, Mapping):
                yield from AttrDict(v, _parent_key=k).items_flat()
            else:
                yield k, v
