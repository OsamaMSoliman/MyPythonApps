import os

from SIC_XE.SIC_XE_InstructionClass import Instruction
from SIC_XE.SIC_XE_Data import *


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
        elif len(splitted) == 1:
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
        if instr.operation.casefold() == "START".casefold() or instr.operation.casefold() == "BASE".casefold() \
                or instr.operation.casefold() == "END".casefold():
            continue  # as the instruction with start has no length
        if instr.operation.casefold() == "BYTE".casefold():
            instruction_length = len(instr.operand) - 3
            if instr.operand.casefold()[0] == "X".casefold():
                instruction_length = round(instruction_length / 2)
        elif instr.operation.casefold() == "WORD".casefold():
            instruction_length = 3
        elif instr.operation.casefold() == "RESW".casefold():
            instruction_length = int(instr.operand) * 3
        elif instr.operation.casefold() == "RESB".casefold():
            instruction_length = int(instr.operand)
        else:
            if instr.operation[0] == "+":
                instruction_length = 4
            else:
                instruction_length = OperationTable[instr.operation].format
        instr.length = instruction_length
        current_address += instruction_length
    return current_address - starting_address


def create_symbol_table(instructions):
    for instr in instructions:
        if instr.label is not None:
            if instr.label not in SymbolTable:
                SymbolTable[instr.label] = instr.address
            else:
                print("ERROR this label is duplicated! : " + instr.label)
    # SymbolTable[None] = "Congratz u triggered a Secret bug !"
    return SymbolTable


def create_obj_codes(instructions):
    obj_codes = []
    for instr in instructions:
        operation = instr.operation.casefold()
        if operation == "RESW".casefold() \
                or operation == "RESB".casefold() \
                or operation == "START".casefold() \
                or operation == "END".casefold():
            instr.obj_code = None
        elif operation == "BASE".casefold():
            instr.obj_code = None
            BaseReg.BaseFlag = True
            BaseReg.setBaseValue()
        elif operation == "NOBASE".casefold():
            instr.obj_code = None
            BaseReg.BaseFlag = False
        elif operation == "WORD".casefold():
            instr.obj_code = instr.get_word_operand()
        elif operation == "BYTE".casefold():
            instr.obj_code = instr.get_byte_operand()
        else:
            calc_object_code(instr)
            BaseReg.check_ldb(instr)
        obj_codes.append(instr.obj_code)
    return obj_codes


def calc_object_code(instr):
    formats = {
        1: format1_2,
        2: format1_2,
        3: format3_4,
        4: format3_4
    }
    return formats[instr.length](instr)


def format1_2(instr):
    # format 1
    obj_code = OperationTable[instr.operation].obj_code
    if instr.length == 1:
        instr.obj_code = obj_code
        return obj_code
    # format 2
    regs = instr.operand.split(',')
    if len(regs) == 1:
        obj_code = "{}{}0".format(obj_code, RegisterTable[regs[0]])
    elif len(regs) == 2:
        obj_code = "{}{}{}".format(obj_code, RegisterTable[regs[0]], RegisterTable[regs[1]])
    else:
        # Error
        print("Error")
    instr.obj_code = obj_code
    return obj_code


def format3_4(instr):
    obj_code = None
    instr.check_addressing_mode()
    target_address = SymbolTable.get(instr.operand)
    if target_address is None:
        if instr.operand is None:  # RSUB case
            instr.obj_code = "4C0000"
            return instr.obj_code
        if instr.operand.isdigit():
            digit_len = len(bin(int(instr.operand))) - 2
            if (instr.addressing_mode & AddressingModes.EXTENDED and digit_len <= 20) or (
                        not (instr.addressing_mode & AddressingModes.EXTENDED) and digit_len <= 12):
                target_address = hex(int(instr.operand))
    if target_address is None:
        # Error
        print("Error")
    elif instr.addressing_mode & AddressingModes.EXTENDED:  # format 4
        obj_code = hex(int(OperationTable[instr.operation].obj_code, 16) << 4 | instr.addressing_mode)
        obj_code = "{:03X}{:05X}".format(int(obj_code, 16), int(target_address, 16))
    else:  # format 3
        if not instr.operand.isdigit():
            target_address, nixbpe = calc_disp(target_address, PC_value=int(instr.address, 16) + instr.length)
            if target_address is None:
                # Error
                print("Error")
            instr.addressing_mode |= nixbpe
        obj_code = hex(int(OperationTable[instr.operation].obj_code, 16) << 4 | instr.addressing_mode)
        obj_code = "{:03X}{:03X}".format(int(obj_code, 16), int(target_address, 16))
    instr.obj_code = obj_code
    return obj_code


def calc_disp(target_address, PC_value):
    nixbpe = AddressingModes.PC_RELATIVE
    # print(target_address, PC_value, BaseReg.BaseValue)
    target_address = int(target_address, 16)
    disp = target_address - PC_value
    if disp < -2048 or disp > 2047:
        if BaseReg.BaseFlag:
            nixbpe = AddressingModes.BASE_RELATIVE
            disp = target_address - BaseReg.BaseValue
            if disp < 0 or disp > 4095:
                return None, 0b0
        else:
            return None, 0b0
    elif disp < 0:  # if we need 2's complement
        disp &= 0xFFF  # let python handle it and return the result by and it with 1s
    return hex(disp), nixbpe


def create_lisfile(instructions):
    with open("lisfile", "w+") as f:
        for instr in instructions:
            f.write(instr.list_file_format())


def create_objfile(instructions, prog_len):
    if NO_ERROR:
        records = []
        h_record = create_h_record(instructions[0], prog_len)
        # print(h_record)
        records.append(h_record)
        d_records = create_d_record()
        # records.extend(d_records)
        r_records = create_r_record()
        # records.extend(r_records)
        t_records = create_t_record(instructions)
        records.extend(t_records)
        m_records = create_m_record(instructions)
        records.extend(m_records)
        e_record = create_e_record(instructions[-1])
        # print(e_record)
        records.append(e_record)
        with open("objfile", "w+") as f:
            for record in records:
                f.write(record + "\n")


def create_h_record(first_instr, prog_len):
    return "H^{:6}^{:06X}^{:06X}".format(first_instr.label, int(first_instr.operand, 16), prog_len)


def create_d_record():
    pass


def create_r_record():
    pass


def create_t_record(instructions):
    t_records = []
    byte_counter = 0
    byte_string = ""
    skip = False
    exceeded30 = False
    temp_byte_string = None
    temp_byte_size = 0
    temp_byte_address = None
    for inst in instructions:
        if not skip:
            byte_starting_address = inst.address
            skip = True
        if exceeded30 or inst.obj_code == None:
            if not byte_counter == 0:
                t_record = "T^{:06X}^{:02X}^{}".format(int(byte_starting_address, 16), byte_counter, byte_string)
                # print(t_record)
                t_records.append(t_record)
            byte_string = ""
            byte_counter = 0
            if exceeded30:
                exceeded30 = False
                byte_string += temp_byte_string + "."
                byte_counter += temp_byte_size
                byte_starting_address = temp_byte_address
            else:
                skip = False
                continue
        if byte_counter + inst.length <= 30:
            byte_string += inst.obj_code + "."
            byte_counter += inst.length
        else:
            temp_byte_string = inst.obj_code
            temp_byte_size = inst.length
            temp_byte_address = inst.address
            exceeded30 = True
    return t_records


def create_m_record(instructions):
    m_records = []
    for instr in instructions:
        if instr.length == 4 and instr.addressing_mode & AddressingModes.DIRECT == AddressingModes.DIRECT:
            # if instr.operand in
            m_record = "M^{:06X}^05^+{}".format(int(instr.address, 16) + 1,
                                                instructions[0].label)  # Debugging :: modify this for External Def/Ref
            # print(m_record)
            m_records.append(m_record)
        elif instr.operation.casefold() == "WORD".casefold() and False:  # Debugging :: modify this for External Def/Ref
            sign = "+/-"
            m_record = "M^{:06X}^06^{}{}".format(int(instr.address, 16) + 1, sign, instructions[0].label)
            print(m_record)
            m_records.append(m_record)
    return m_records


def create_e_record(end_instr):
    if SymbolTable.get(end_instr.operand) is not None:
        return "E^{:06X}".format(int(SymbolTable[end_instr.operand], 16))
