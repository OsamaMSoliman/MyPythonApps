import os
from SIC_XE.SIC_XE_Data import *
from SIC_XE.SIC_XE_Literal import *


def decimal(hex_str):
    return int(hex_str, 16)


def hex_string(decimal_num):
    return hex(decimal_num)[2:]


def read_file(file_name):
    file_name = "ExamplePrograms/" + file_name
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
        # check if it's a comment or an empty line ((((comments must be on a separate line))))
        if line.strip().startswith('.') or len(line.strip()) == 0:
            continue
        splitted = line.split()
        if len(splitted) == 3:
            instr = Instruction(label=splitted[0], operation=splitted[1], operand=splitted[2])
        elif len(splitted) == 2:
            instr = Instruction(label=None, operation=splitted[0], operand=splitted[1])
        elif len(splitted) == 1:
            instr = Instruction(label=None, operation=splitted[0], operand=None)
        else:
            ERROR.NO_ERROR = False
            instr = None
            # Debugging:: how should this error appear to the user?
        instructions.append(instr)
    return instructions


def calc_addresses(instructions):
    starting_address = 0x0000
    first_instr = instructions[0]
    if first_instr.operation.casefold() == "START".casefold():
        starting_address = decimal(first_instr.operand)
    current_address = starting_address
    for instr in instructions:
        instr.address = hex_string(current_address)
        operation = instr.operation.casefold()
        if operation == "START".casefold() or operation == "BASE".casefold() \
                or operation == "NOBASE".casefold():
            continue  # as the instruction with start has no length
        elif operation == "LTORG".casefold() or operation == "END".casefold():
            # create literal pool then add it to the instruction list
            instruction_length, literal_instructions = create_literal_pool(current_address)
            temp_counter = instructions.index(instr)
            for literal_instruction in literal_instructions:
                temp_counter += 1
                instructions.insert(temp_counter, literal_instruction)
            current_address += instruction_length
            continue
        if operation == "BYTE".casefold():
            instruction_length = len(instr.operand) - 3
            if instr.operand.casefold()[0] == "X".casefold():
                instruction_length = round(instruction_length / 2)
        elif operation == "WORD".casefold():
            instruction_length = 3
        elif operation == "RESW".casefold():
            instruction_length = int(instr.operand) * 3
        elif operation == "RESB".casefold():
            instruction_length = int(instr.operand)
        else:
            if instr.operation[0] == "+":
                instruction_length = 4
            elif instr.operation.startswith('='):
                continue
            else:
                instruction_length = OperationTable[instr.operation].format
        instr.length = instruction_length
        current_address += instruction_length
        # check for literal in operand if so process it
        check_for_literal(instr.operand, current_address)
    return current_address - starting_address


def create_symbol_table(instructions):
    for instr in instructions:
        if instr.label is not None:
            if instr.label == '*':
                continue
            elif instr.label not in SymbolTable:
                if instr.operation.casefold() == "EQU".casefold():
                    SymbolTable[instr.label] = Symbol(False, instr.operand)
                else:
                    SymbolTable[instr.label] = Symbol(True, instr.address)
            else:
                ERROR.NO_ERROR = False
                instr.error = ERROR.Duplicated_Label + instr.label
                print(instr.error)
                # SymbolTable[None] = "Congratz u triggered a Secret bug !"


def process_operand(operand):
    relative, value = True, None
    return relative, value


def create_obj_codes(instructions):
    for instr in instructions:
        operation = instr.operation.casefold()
        if operation.startswith('=') \
                or operation == "RESW".casefold() \
                or operation == "RESB".casefold() \
                or operation == "START".casefold() \
                or operation == "END".casefold() \
                or operation == "LTORG".casefold():
            instr.obj_code = None
        elif operation == "BASE".casefold():
            instr.obj_code = ""
            BaseReg.BaseFlag = True
            BaseReg.setBaseValue()
            print(BaseReg.BaseValue)
        elif operation == "NOBASE".casefold():
            instr.obj_code = ""
            BaseReg.BaseFlag = False
        elif operation == "WORD".casefold():
            instr.obj_code = instr.get_word_operand()
        elif operation == "BYTE".casefold():
            instr.obj_code = instr.get_byte_operand()
        else:
            calc_object_code(instr)
            BaseReg.check_ldb(instr)


def calc_object_code(instr):
    if OperationTable.get(instr.get_operation()) is None:
        ERROR.NO_ERROR = False
        instr.error = ERROR.Undefined_Operation + instr.operation
        print(instr.error)
        return
    return {
        1: format1_2,
        2: format1_2,
        3: format3_4,
        4: format3_4
    }[instr.length](instr)


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
        ERROR.NO_ERROR = False
        instr.error = ERROR.Unknown_Format
        print(instr.error)
    instr.obj_code = obj_code
    return obj_code


def format3_4(instr):
    obj_code = None
    instr.check_addressing_mode()
    target_address = None
    if instr.operand is not None and instr.operand.startswith('='):
        target_address = Literal.get_address_from_table(instr.operand)
        print(target_address)
    else:
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
        ERROR.NO_ERROR = False
        instr.error = ERROR.Undefined_Symbol + instr.operand
        print(instr.error)
    elif instr.addressing_mode & AddressingModes.EXTENDED:  # format 4
        obj_code = hex(int(OperationTable[instr.operation].obj_code, 16) << 4 | instr.addressing_mode)
        obj_code = "{:03X}{:05X}".format(int(obj_code, 16), int(target_address, 16))
    else:  # format 3
        if not instr.operand.isdigit():
            target_address, nixbpe = calc_disp(target_address, PC_value=int(instr.address, 16) + instr.length)
            if target_address is None:
                ERROR.NO_ERROR = False
                instr.error = ERROR.Out_Of_Range if nixbpe else ERROR.Use_Base
                print(instr.error)
                return None
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
                return None, 0b1
        else:
            return None, 0b0
    elif disp < 0:  # if we need 2's complement
        disp &= 0xFFF  # let python handle it and return the result by and it with 1s
    return hex(disp), nixbpe


def create_lisfile(filename, instructions):
    with open("ExamplePrograms/OUTPUT/" + filename + "_lisfile", "w+") as f:
        for instr in instructions:
            f.write(instr.list_file_format())


def create_objfile(filename, instructions, prog_len):
    if ERROR.NO_ERROR:
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
        # m_records = create_m_record(instructions)
        # records.extend(m_records)
        for i in range(len(instructions) - 1, 0, -1):
            if instructions[i].operation.casefold() == "END".casefold():
                e_record = create_e_record(instructions[i])
                # print(e_record)
                records.append(e_record)
                break
        with open("ExamplePrograms/OUTPUT/" + filename + "_objfile", "w+") as f:
            for record in records:
                f.write(record + "\n")
    return not ERROR.NO_ERROR


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
