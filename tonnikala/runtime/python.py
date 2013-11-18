from __future__ import absolute_import, division, print_function, unicode_literals

NoneType = type(None)

from .rope import Rope
from ..helpers import escape as strescape
from six import text_type

def escape(obj):
    if isinstance(obj, Buffer):
        return obj

    return strescape(text_type(obj))


class Buffer(Rope):
    def __init__(self, initial_contents=None):
        super(Buffer, self).__init__(initial_contents or [])
        self.rope_call = super(Buffer, self).__call__


    def escape(self, obj):
        self.rope_call(escape(obj))
        return self


    def output_boolean_attr(self, name, value):
        if isinstance(value, (bool, NoneType)):
            if bool(value):
                self.rope_call(' ', name, '=', name)

            # skip on false, None
            return

        self.rope_call(' ', name, '="', escape(value), '"')
        return self


class AttrBuffer(Rope):
    def __init__(self):
        super(AttrBuffer, self).__init__()
        self.boolean_value = None
        self.count = 0
        self.rope_call = super(AttrBuffer, self).__call__

    def escape(self, obj):
        self.count += 1
        self.boolean_value = None
        if self.count == 1 and isinstance(obj, (bool, NoneType)):
            self.boolean_value = bool(obj)

        self.rope_call(escape(obj))
        return self

    def __call__(self, obj):
        self.rope_call(obj)
        self.count += 1
        self.boolean_value = None
        return self


def make_buffer(*args):
    return Buffer(list(args))


def make_buffer_from_list(thelist):
    return Buffer(thelist)


def output_attrs(values):
    if not values:
        return ''

    values = dict(values)
    rv = Buffer()
    for k, v in values.items():
        if isinstance(v, (bool, NoneType)):
            if v:
                v = k
            else:
                continue

        rv(' ')
        rv(k)
        rv('="')
        rv(escape(v))
        rv('"')

    return rv

def output_attr(name, value_func):
    contents = value_func()
    if contents.boolean_value != None:
        if not contents.boolean_value:
            return ''
        else:
            return ' %s="%s"' % (name, name)

    return make_buffer_from_list([' ' + name + '="'] + contents._buffer + ['"'])

def import_defs(href):
    return {}
