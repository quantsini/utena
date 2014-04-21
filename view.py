# -*- coding: utf-8 -*-
import io
from collections import namedtuple
from struct import Struct


def makes_header(name, byte_order='@', *name_format_tuples):
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


SceneHeader = makes_header('SceneHeader', '<',
                           ('file_type', '4s'),
                           ('file_size', 'I'),
                           ('start_data', 'H'),
                           ('start_script', 'H'),
                           ('unk1', 'H'))


TextHeader = makes_header('TextHeader', '<',
                          ('ptr_beg_1', 'B'),
                          ('diag_ptr', 'H'),
                          ('ptr_end_1', 'H'),

                          ('ptr_beg_2', 'B'),
                          ('tag_ptr', 'H'),
                          ('ptr_end_2', 'H'),

                          ('unk1', 'B'),
                          ('unk2', 'H'),
                          ('end_code', 'B'),

                          ('zero', 'B'))


# Need to somehow compute this value
pointer_block_start = 7807


class Scene:

    def __init__(self, buff, header):
        self._header = header
        self._buff = buff

    @property
    def texts(self):
        for offset in range(pointer_block_start, self._header.start_script, TextHeader.header_format.size):
            current_header = TextHeader.from_buffer(self._buff, offset)
            next_offset = offset + TextHeader.header_format.size
            if next_offset < self._header.start_script:
                next_header = TextHeader.from_buffer(self._buff, next_offset)
                size = next_header.tag_ptr - current_header.tag_ptr
            else:
                size = 99999 # lol
            yield Text(self._buff, current_header, size)


class Text:

    def __init__(self, buff, text_header, size):
        self._header = text_header
        self._buff = buff
        self._size = size

    @property
    def data(self):
        self._buff.seek(self._header.tag_ptr)
        data = self._buff.read(self._size)
        data = data.replace(b'\x0e', b'\n')
        return data.decode('shiftjis')

    @property
    def voice_track(self):
        voice_track, _, _ = self.data.split('\x00')
        return voice_track

    @property
    def dialog(self):
        _, dialog, _ = self.data.split('\x00')
        return dialog

file = 'DAY_A0.SCN'
file = 'DAY_D2.SCN'

f = io.open(file, 'rb')

header = SceneHeader.from_buffer(f)
scene = Scene(f, header)

for text in scene.texts:
    print(text._header)
    print(repr(text.data))
