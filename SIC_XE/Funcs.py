import os


class Instruction(object):
    address = None

    def __init__(self, label, operation, operand):
        self.label = label
        self.operation = operation
        self.operand = operand


def read_file(file_name):
    if os.path.isfile(file_name):
        lines = []
        with open(file_name) as f:
            lines.append(f.readline())
        return lines


def parse_line(lines):
    instructions = []
    instr = None
    for line in lines:
        splitted = line.split()
        if len(splitted) == 3:
            instr = Instruction(label=splitted[0], operation=splitted[1], operand=splitted[2])
        elif len(splitted) == 2:
            instr = Instruction(label=None, operation=splitted[0], operand=splitted[1])
        instructions.append(instr)
    return instructions


def calc_addresses(instructions):
    current_address = 0x0000
    first_instr = instructions[0]
    if first_instr.operation.casefold() == "START".casefold():
        current_address = int(first_instr.operand, 16)
    instruction_length = 0x3
    for instr in instructions:
        if instr.operation.casefold() == "BYTE".casefold():
            instruction_length = len(instr.operand)/2
        else:
            instruction_length = 0x3
        current_address += instruction_length



def create_symbol_table(instructions):
    symbol_table = {}
    for instr in instructions:
        if instr.label is not None:
            if instr.label not in symbol_table:
                symbol_table[instr.label] = instr.address
            else:
                print("ERROR this label is duplicated! : " + instr.label)
