# -*- coding: utf-8 -*-
from sh2.parse_opcode_csv import load_from_csv


instruction_schemas = set(load_from_csv('sh2/opcodes.csv'))


def load_instruction_schemas():
    return instruction_schemas
