def get_target_address(addressing_mode, sym_table_value):
    return AddressingModes.TA[addressing_mode](sym_table_value)[2:]


def direct(sym_table_value):
    return sym_table_value


def indexed(sym_table_value):
    return hex(0x8000 + int(sym_table_value, 16))


class AddressingModes(object):
    DIRECT = "direct"
    INDEXED = "indexed"

    TA = {
        DIRECT: direct,
        INDEXED: indexed
    }
