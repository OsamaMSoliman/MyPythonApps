from SIC_XE.OPTAB import *
from SIC_XE.SIC_Funcs import *
from SIC_XE.UnitTest import *


def SIC():
    # first_path
    lines = read_file("example.txt")
    instructions = parse_lines(lines)
    prog_length = calc_addresses(instructions)
    symbol_table = create_symbol_table(instructions)

    # second_path
    object_codes = create_obj_codes(instructions, symbol_table, OPTAB)


def SIC_XE():
    pass


def run(filename, is_test, machine_type):
    if is_test:
        lines = test_read_file(filename)
        instructions = test_parse_lines(lines)
        prog_length = calc_addresses(instructions, OPTABXE)
        symbol_table = test_create_symbol_table(instructions)
        object_codes = test_create_obj_codes(instructions, symbol_table, OPTABXE)
    elif machine_type == "SIC":
        SIC()
    elif machine_type == "SIC_XE":
        SIC_XE()


if __name__ == "__main__":
    run(filename="exampleXE.txt", is_test=True, machine_type="SIC")
