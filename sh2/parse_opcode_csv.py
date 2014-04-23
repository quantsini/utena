# -*- coding: utf-8 -*-
from collections import namedtuple
import csv


Instruction = namedtuple('Instruction', 'opcode name input_format')


def convert(opcode):
    # xorable
    opcode = opcode.replace('i', '0')
    opcode = opcode.replace('n', '0')
    opcode = opcode.replace('m', '0')
    opcode = opcode.replace('d', '0')
    return opcode

opcodes = set()
with open('opcodes.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in reader:
        name, format, opcode = [el.strip() for el in row]
        opcode = convert(opcode)
        opcodes.add(opcode)

    # assert all opcodes are not ambigious
    assert len(opcodes) == 142