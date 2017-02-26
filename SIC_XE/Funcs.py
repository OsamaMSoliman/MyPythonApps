import os


class Instruction(object):
    address = None

    def __init__(self, label, operation, operand):
        self.label = label
        self.operation = operation
        self.operand = operand

    def get_word_operand(self):
        return hex(self.operand)[2:]

    def get_byte_operand(self):
        first_letter = self.operand[0].casefold()
        if first_letter == "C".casefold():
            return "".join([hex(ord(char))[2:] for char in self.operand[2:-1]])
        elif first_letter == "X".casefold():
            return self.operand[2:-1]


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
    for instr in instructions:
        if instr.operation.casefold() == "BYTE".casefold():
            instruction_length = round(len(instr.operand) / 2)
        else:
            instruction_length = 0x3
        current_address += instruction_length
        instr.address = hex(current_address)


def create_symbol_table(instructions):
    symbol_table = {}
    for instr in instructions:
        if instr.label is not None:
            if instr.label not in symbol_table:
                symbol_table[instr.label] = instr.address
            else:
                print("ERROR this label is duplicated! : " + instr.label)
    return symbol_table


def create_obj_code(instructions, sym_table, op_table):
    obj_codes = []
    for instr in instructions:
        operation = instr.operation.casefold()
        if operation == "RESW".casefold() \
                or operation == "RESB".casefold() \
                or operation == "START".casefold() \
                or operation == "END".casefold():
            obj_codes.append(None)
        elif operation == "WORD".casefold():
            obj_codes.append(instr.get_word_operand())
        elif operation == "BYTE".casefold():
            obj_codes.append(instr.get_byte_operand())
        else:
            obj_code = "%s%s".format(op_table[instr.operation], sym_table[instr.operand])
            if instr.operand[-2:].casefold() == ",X".casefold():  # no need to check for length as we use ':'
                obj_code = hex(0x8000 + int(obj_code, 16))[2:]
            obj_codes.append(obj_code)
    return obj_codes
