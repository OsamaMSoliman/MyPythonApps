# def SIC():
#     # first_path
#     lines = read_file("example.txt")
#     instructions = parse_lines(lines)
#     prog_length = calc_addresses(instructions)
#     symbol_table = create_symbol_table(instructions)
#
#     # second_path
#     object_codes = create_obj_codes(instructions, symbol_table, OPTAB)
#
import sys

from SIC_XE.SIC_XE_methods import *


def first_path(filename):
    lines = read_file(filename)
    instructions = parse_lines(lines)
    prog_len = calc_addresses(instructions)
    create_symbol_table(instructions)
    return prog_len, instructions


def second_path(filename, instructions, prog_len):
    create_obj_codes(instructions)
    create_lisfile(filename, instructions)
    error = create_objfile(filename, instructions, prog_len)
    if error:
        print("ERROR! plz check list file")
    else:
        print("Done !")


def run(filename):
    prog_len, instructions = first_path(filename)
    second_path(filename, instructions, prog_len)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run(filename="exampleXE")
    elif len(sys.argv) == 2:
        run(filename=sys.argv[1])