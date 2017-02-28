import os

from SIC_XE.AddressingModesClass import get_target_address
from SIC_XE.InstructionClass import Instruction


def read_file(file_name):
    if os.path.isfile(file_name):
        lines = []
        with open(file_name) as f:
            for line in f.readlines():
                lines.append(line)
        return lines


def parse_lines(lines):
    instructions = []
    instr = None
    for line in lines:
        splitted = line.split()
        if len(splitted) == 3:
            instr = Instruction(label=splitted[0], operation=splitted[1], operand=splitted[2])
        elif len(splitted) == 2:
            instr = Instruction(label=None, operation=splitted[0], operand=splitted[1])
        elif len(splitted) == 2:
            instr = Instruction(label=None, operation=splitted[0], operand=None)
        instructions.append(instr)
    return instructions


def calc_addresses(instructions):
    starting_address = 0x0000
    first_instr = instructions[0]
    if first_instr.operation.casefold() == "START".casefold():
        starting_address = int(first_instr.operand, 16)
    current_address = starting_address
    for instr in instructions:
        instr.address = hex(current_address)
        if instr.operation.casefold() == "START".casefold():
            continue  # as the instruction with start has no length
        if instr.operation.casefold() == "BYTE".casefold():
            instruction_length = round(len(instr.operand) / 2)
        else:
            instruction_length = 0x3
        current_address += instruction_length
    return current_address - starting_address


def create_symbol_table(instructions):
    symbol_table = {}
    for instr in instructions:
        if instr.label is not None:
            if instr.label not in symbol_table:
                symbol_table[instr.label] = instr.address
            else:
                print("ERROR this label is duplicated! : " + instr.label)
    return symbol_table


def create_obj_codes(instructions, sym_table, op_table):
    obj_codes = []
    for instr in instructions:
        operation = instr.operation.casefold()
        if operation == "RESW".casefold() \
                or operation == "RESB".casefold() \
                or operation == "START".casefold() \
                or operation == "END".casefold():
            instr.obj_code = None
        elif operation == "WORD".casefold():
            instr.obj_code = instr.get_word_operand()
        elif operation == "BYTE".casefold():
            instr.obj_code = instr.get_byte_operand()
        else:
            instr.check_addressing_mode()
            target_address = get_target_address(instr.addressing_mode, sym_table[instr.operand])
            obj_code = "{}{}".format(op_table[instr.operation], target_address)
            instr.obj_code = obj_code
        obj_codes.append(instr.obj_code)
    return obj_codes
