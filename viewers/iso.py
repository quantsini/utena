# -*- coding: utf-8 -*-
import io
import struct
from pprint import pprint
from util.structs import makes_header_struct
from sh2 import opcodes


IPStruct = makes_header_struct('IPStruct', '<',
   ('hardware_identifier', '16s'),
   ('maker_id', '16s'),
   ('product_number', '10s'),
   ('version', '6s'),
   ('release_date', '8s'),
   ('device_information', '8s'),
   ('compatible_area_symbols', '10s'),
   ('space', '6s'),
   ('compatible_peripherals', '16s'),
   ('game_title', '112s'),
   ('reserved', '16s'),
   ('ipsize', 'L'),
   ('reserved2', 'L'),
   ('stack_m', 'L'),
   ('stack_s', 'L'),
   ('first_read_address', 'L'),
   ('first_read_size', 'L'),
   ('reserved3', 'L'),
   ('reserved4', 'L'))


class UnknownOpcode(Exception): pass


if __name__ == '__main__':
    file = 'original_game_files/Utena_Sega1.iso'

    with io.open(file, 'rb') as f:
        ip_struct = IPStruct.from_buffer(f)
        pprint(ip_struct)
        f.seek(ip_struct.first_read_address)
        for _ in range(int(ip_struct.first_read_size/2)):
            opcode = f.read(2)
            raw_instruction = struct.unpack('<H', opcode)[0]
            instruction = opcodes.lookup(raw_instruction)
            print(instruction)
