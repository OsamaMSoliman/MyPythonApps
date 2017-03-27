def get_target_address(addressing_mode, operand):
    if addressing_mode is None:
        return "0000"  # 0x0000
    else:
        nixbpe = addressing_mode
        addressing_mode &= 0b110000
    return AddressingModes.TA[addressing_mode](nixbpe, operand)[2:]


def direct(nixbpe, operand):
    # check if PC relative or Base relative
    # then call the appropriate function
    return "NOT YET"


def indexed(sym_table_value):
    return hex(0x8000 + int(sym_table_value, 16))


def indirect(sym_table_value):
    return "NOT YET"


def extended(sym_table_value):
    return "NOT YET"


def immediate(sym_table_value):
    return "NOT YET"


def pc_r(sym_table_value):
    pass


def base_r(sym_table_value):
    pass


class AddressingModes(object):
    IMMEDIATE = 0b010000
    INDIRECT =  0b100000
    DIRECT =    0b110000

    PC_RELATIVE =   0b110010
    BASE_RELATIVE = 0b110100

    INDEXED =   0b001000
    EXTENDED =  0b000001

    TA = {
        DIRECT: direct,
        INDIRECT: indirect,
        IMMEDIATE: immediate
    }
