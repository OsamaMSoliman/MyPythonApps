from SIC_XE.OPTAB import OPTAB
from SIC_XE.UnitTest import *
from SIC_XE.SIC_Funcs import *


def first_path():
    lines = read_file("example.txt")
    instructions = parse_lines(lines)
    prog_length = calc_addresses(instructions)
    symbol_table = create_symbol_table(instructions)
    object_codes = create_obj_codes(instructions, symbol_table, OPTAB)


def second_path():
    pass


def run(is_test):
    if is_test:
        lines = test_read_file("example.txt")
        instructions = test_parse_lines(lines)
        prog_length = test_calc_addresses(instructions)
        symbol_table = test_create_symbol_table(instructions)
        object_codes = test_create_obj_codes(instructions, symbol_table, OPTAB)
    else:
        first_path()
        second_path()


if __name__ == "__main__":
    run(is_test=True)
