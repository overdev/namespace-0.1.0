# !/usr/bin/python
# -*- coding: utf-8 -*-

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Jorge
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import ast
import io
from collections import OrderedDict


__all__ = {
    'Namespace',
}


class Namespace(object):

    _indent = 0

    @classmethod
    def load(cls, fname):
        # type: (str) -> Namespace
        if isinstance(fname, io.TextIOWrapper):
            with fname as ns:
                code = "".join(ns.readlines())
        else:
            with open(fname) as ns:
                code = "".join(ns.readlines())
        subdat = ast.literal_eval(code)
        return cls(**subdat)

    @classmethod
    def items(cls, ns):
        # type: (Namespace) -> tuple
        assert ns.__class__ is cls, "'ns' is not a Namespace object."
        return ns._dict.items()

    @classmethod
    def keys(cls, ns):
        # type: (Namespace) -> tuple
        assert ns.__class__ is cls, "'ns' is not a Namespace object."
        return ns._dict.keys()

    @classmethod
    def values(cls, ns):
        # type: (Namespace) -> tuple
        assert ns.__class__ is cls, "'ns' is not a Namespace object."
        return ns._dict.values()

    def __init__(self, **kwargs):
        self._dict = OrderedDict()
        for key in kwargs:
            value = kwargs[key]
            if isinstance(value, (dict, OrderedDict)):
                self[key] = Namespace(**value)
            else:
                setattr(self, key, value)

    def __getattr__(self, name):
        if name != '_dict':
            if name in getattr(self, '_dict'):
                return getattr(self, '_dict')[name]
            else:
                raise AttributeError("Namespace object has no '{}' attribute.".format(name))
        else:
            return self._dict

    def __setattr__(self, name, value):
        if name != '_dict':
            if isinstance(value, (dict, OrderedDict)):
                getattr(self, '_dict')[name] = Namespace(**value)
            else:
                getattr(self, '_dict')[name] = value
        else:
            getattr(self, '__dict__')[name] = value

    def __delattr__(self, name):
        if name == '_dict':
            raise AttributeError("Could not delete the attribute.")
        else:
            if name in getattr(self, '_dict'):
                del getattr(self, '_dict')[name]
            else:
                raise AttributeError("Namespace object has no '{}' attribute.".format(name))

    def __str__(self):
        Namespace._indent += 1
        indents = " " * (Namespace._indent * 4)
        _items = ""
        for key in self._dict:
            _items += "{}'{}': {},\n".format(indents, key, repr(self._dict[key]))
        Namespace._indent -= 1
        return "{{\n{}{}}}".format(_items, ' ' * (Namespace._indent * 4))

    __repr__ = __str__

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            self._dict.__setitem__(key, Namespace(**value))
        else:
            self._dict.__setitem__(key, value)

    def __delitem__(self, key):
        self._dict.__delitem__(key)

    def __len__(self):
        return self._dict.__len__()

    def __iter__(self):
        return self._dict.__iter__()

    def __contains__(self, name):
        return name in self._dict
