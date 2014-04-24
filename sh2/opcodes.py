# -*- coding: utf-8 -*-
from collections import namedtuple
from sh2 import instruction_schema_repository as repository
from sh2.instruction_schema import valid_arg_types


Instruction = namedtuple('Instruction', 'command args')
Args = namedtuple('Args', ' '.join(valid_arg_types))


class UnknownInstruction(Exception): pass


def lookup(instruction):
    instruction_schema = _match_instruction_schema(instruction)
    args = _extract_args(instruction_schema, instruction)
    return Instruction(instruction_schema.command, args)

def _match_instruction_schema(instruction):
    instruction_schemas = repository.load_instruction_schemas()

    for instruction_schema in instruction_schemas:
        opcode_schema = instruction_schema.opcode_schema
        if opcode_schema.mask & instruction == opcode_schema.signature:
            return instruction_schema
    else:
        raise UnknownInstruction(bin(instruction))

def _extract_args(instruction_schema, instruction):
    arg_masks = instruction_schema.arg_masks
    kwargs = {}
    for valid_arg_type in valid_arg_types:
        kwargs[valid_arg_type] = None
        mask = getattr(arg_masks, valid_arg_type)
        if mask is not None:
            data = instruction & mask
            while mask & 1 == 0:
                data = data >> 1
                mask = mask >> 1
            kwargs[valid_arg_type] = data
    return Args(**kwargs)
