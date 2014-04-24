# -*- coding: utf-8 -*-
from collections import namedtuple


valid_arg_types = ['i', 'm', 'n', 'd']


class InstructionSchema(namedtuple('Instruction', 'command opcode_schema arg_schema')):

    def matches(self, instruction):
        return self.opcode_schema.matches(instruction)

    def extract_args(self, instruction):
        pass


OpcodeSchema = namedtuple('Opcode', 'mask signature')


Args = namedtuple('Args', ' '.join(valid_arg_types))


class ArgSchema(namedtuple('ArgSchema', 'i_mask n_mask m_mask d_mask')):
    pass


def strip_args(code):
    for valid_arg_type in valid_arg_types:
        code = code.replace(valid_arg_type, '0')
    return code


def build_opcode_schema(code):
    mask = code.replace('0', '1')
    mask = strip_args(mask)
    mask = int(mask, 2)
    signature = strip_args(code)
    signature = int(signature, 2)
    return OpcodeSchema(mask, signature)


def build_arg_schema(code):
    for valid_arg_type in valid_arg_types:
        left = code.find(valid_arg_type)
        right = code.rfind(valid_arg_type)
        code[left:right]
        import ipdb ; ipdb.set_trace()
        pass


def build_instruction_schema(name, code):
    opcode_schema = build_opcode_schema(code)
    arg_schema = build_arg_schema(code)
    return InstructionSchema(name, opcode_schema, arg_schema)
