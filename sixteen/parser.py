# -*- coding: utf-8 -*-

import re
from sixteen.dcpu16 import DCPU16
from sixteen.words import from_opcode


class _meta_parser(type):
    """A metaclass that collects all the @parse methods into a list of pairs
    named __parse_methods__; we'll use this for Parsers.
    """
    def __new__(cls, name, bases, dictionary):
        __parse_methods__ = []
        for k, v in dictionary.iteritems():
            if getattr(v, "pattern", None):
                __parse_methods__.append((v.pattern, v))
        dictionary["__parse_methods__"] = __parse_methods__
        return type(name, bases, dictionary)


def parse(pattern):
    """Given a pattern to use as a regular expression, return a decorator that
    sets that function's "pattern" attribute to that pattern.
    """
    def parser_decorator(fn):
        fn.pattern = pattern
        return fn
    return parser_decorator


class Parser(object):
    "A base class for parsers."
    __metaclass__ = _meta_parser

    def parse(self, token):
        "Check all of the __parse_methods__ for a parser that matches this."
        for pattern, method in self.__parse_methods__:
            m = re.match(pattern, token)
            if m:
                return method(self, *m.groups())
        else:
            # oh no, nothing matched.
            return None


class AssemblyParser(Parser):
    # why doesn't this get inherited from Parser?
    __metaclass__ = _meta_parser

    registers = ["A", "B", "C", "X", "Y", "Z", "I", "J"]
    rs = r"([a-cx-zijA-CX-ZIJ])"

    @parse(rs)
    def register(self, name):
        return self.registers.index(name.upper())

    @parse(r"\[%s\]" % rs)
    def register_pointer(self, name):
        n = self.registers.index(name.upper())
        return 0x08 + n