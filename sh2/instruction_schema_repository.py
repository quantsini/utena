# -*- coding: utf-8 -*-
from sh2.parse_opcode_csv import load_from_csv


instruction_schemas = load_from_csv('sh2/opcodes.csv')


class UnknownOpcodeError(Exception): pass


def lookup(instruction):
    for instruction_schema in instruction_schemas:
        instruction_schema.opcode_schema.mask & instruction ==
        if instruction_schema.matches(instruction):
            return instruction_schema
    else:
        raise UnknownOpcodeError(bin(instruction))
