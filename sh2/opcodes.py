# -*- coding: utf-8 -*-
from sh2 import repository


from collections import namedtuple


Instruction = namedtuple('Instruction', 'command args')
class UnknownInstruction(Exception): pass


def lookup(instruction):
    instruction_schema = _match_instruction_schema(instruction)
    args = instruction_schema.extract_args(instruction)
    return Instruction(instruction_schema.command, args)

def _match_instruction_schema(instruction):
    instruction_schemas = repository.load_instruction_schemas()

    for instruction_schema in instruction_schemas:
        if instruction_schema.matches(instruction):
            return instruction_schema
    else:
        raise UnknownInstruction(bin(instruction))
