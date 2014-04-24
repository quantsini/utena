# -*- coding: utf-8 -*-
from collections import namedtuple


valid_arg_types = ['i', 'm', 'n', 'd']


InstructionSchema = namedtuple('Instruction', 'command opcode_schema arg_masks')


OpcodeSchema = namedtuple('OpcodeSchema', 'mask signature')


class ArgMasks(namedtuple('ArgMasks', ' '.join(valid_arg_types))):
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


def build_arg_masks(code):
    kwargs = {}
    for valid_arg_type in valid_arg_types:
        kwargs[valid_arg_type] = None
        left = code.find(valid_arg_type)
        right = code.rfind(valid_arg_type) + 1
        if left != -1:
            mask = (2 ** (right - left) - 1) << (16 - right)
            kwargs[valid_arg_type] = mask
    return ArgMasks(**kwargs)

def build_instruction_schema(name, code):
    opcode_schema = build_opcode_schema(code)
    arg_masks = build_arg_masks(code)
    return InstructionSchema(name, opcode_schema, arg_masks)
