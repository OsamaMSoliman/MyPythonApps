from SIC_XE.SIC_Funcs import *


def test_print(things):
    count = 0
    if isinstance(things, list):
        for thing in things:
            print(str(count), "\t", str(thing))
            count += 1
    elif isinstance(things, dict):
        for k, v in things.items():
            print(str(count), "\t", str(k), "\t", str(v))
            count += 1
    print("\n<======================>")


def test_read_file(file_name):
    print(">>> test_read_file :-")
    lines = read_file(file_name)
    test_print(lines)
    return lines


def test_parse_lines(lines):
    print(">>> test_parse_lines :-")
    inst = parse_lines(lines)
    test_print(inst)
    return inst


def test_calc_addresses(instructions):
    print(">>> test_calc_addresses :-")
    prog_length = calc_addresses(instructions)
    print(prog_length)
    test_print(instructions)
    return prog_length


def test_create_symbol_table(instructions):
    print(">>> test_create_symbol_table :-")
    symbol_table = create_symbol_table(instructions)
    test_print(symbol_table)
    return symbol_table


def test_create_obj_codes(instructions, symbol_table, OPTAB):
    print(">>> test_create_obj_codes :- ")
    object_codes = create_obj_codes(instructions, symbol_table, OPTAB)
    test_print(instructions)
    test_print(object_codes)
    return object_codes
