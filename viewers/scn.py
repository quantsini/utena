# -*- coding: utf-8 -*-
import io
from util.structs import makes_header_struct


SceneHeader = makes_header_struct('SceneHeader', '<',
                           ('file_type', '4s'),
                           ('file_size', 'I'),
                           ('start_data', 'H'),
                           ('start_script', 'H'),
                           ('unk1', 'H'))


TextHeader = makes_header_struct('TextHeader', '<',
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


class Scene:

    def __init__(self, buff, header, pointer_block_start):
        self._header = header
        self._buff = buff
        self._pointer_block_start = pointer_block_start

    @property
    def texts(self):
        for offset in range(self._pointer_block_start, self._header.start_script, TextHeader.header_format.size):
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
        return self._buff.read(self._size)


if __name__ == '__main__':
    file = 'original_game_files/Utena_Sega1/SCNBIN/DAY_A0.SCN'
    file = 'original_game_files/Utena_Sega1/SCNBIN/DAY_A1.SCN'

    # Need to somehow compute this value
    pointer_block_start = 7807

    with io.open(file, 'rb') as f:
        header = SceneHeader.from_buffer(f)

        scene = Scene(f, header, pointer_block_start)

        for text in scene.texts:
            print(text._header)
            print(repr(text.data.decode('shiftjis')))
