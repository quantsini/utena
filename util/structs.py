# -*- coding: utf-8 -*-
from collections import namedtuple
from struct import Struct


def makes_header_struct(name, byte_order='@', *name_format_tuples):
    """Factory method for creating header types"""
    names, formats = zip(*name_format_tuples)
    class _Header(namedtuple('_Header', ' '.join(names))):
        header_format = Struct('<' + ''.join(formats))
        @classmethod
        def from_buffer(cls, buff, start=0):
            buff.seek(start)
            data = buff.read(cls.header_format.size)
            header_data = cls.header_format.unpack_from(data)
            return cls._make(header_data)
    _Header.__name__ = name
    return _Header
