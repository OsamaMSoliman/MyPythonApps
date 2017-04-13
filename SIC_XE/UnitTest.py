from SIC_XE.SIC_XE_methods import *


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


def test_create_obj_codes(instructions):
    print(">>> test_create_obj_codes :- ")
    object_codes = create_obj_codes(instructions)
    test_print(instructions)
    test_print(object_codes)
    return object_codes


def test_similarObjectCodes(objlist):
    list = ["17202D", "69202D", "4B101036", "032026", "290000", "332007", "4B10105D", "3F2FEC", "032010", "0F2016",
            "010003", "0F200D", "4B10105D", "3E2003", "454F46", "B410", "B400", "B440", "75101000", "E32019", "332FFA",
            "DB2013", "A004", "332008", "57C003", "B850", "3B2FEA", "134000", "4F0000", "F1", "B410", "774000",
            "E32011", "332FFA", "53C003", "DF2008", "B850"]
    i, j = 0, 0
    while i < len(list) and j < len(objlist):
        while objlist[j] is None:
            print("None")
            j += 1
        print(i, list[i], " )_( ", objlist[j], end="")
        if list[i] == objlist[j]:
            print()
        else:
            print("     <== ")
        i += 1
        j += 1


def test_OPTAB_Duplicates():
    dic = {}
    for e in OperationTable:
        if OperationTable[e].obj_code in dic:
            dic[OperationTable[e].obj_code] += 1
            print(e, OperationTable[e].obj_code, " <= Duplicate")
        else:
            dic[OperationTable[e].obj_code] = 0



def run_test():
    lines = test_read_file("exampleXE.txt")
    instructions = test_parse_lines(lines)
    prog_len = test_calc_addresses(instructions)
    test_create_symbol_table(instructions)
    obj_codes = test_create_obj_codes(instructions)
    test_similarObjectCodes(obj_codes)
    test_OPTAB_Duplicates()



if __name__ == "__main__":
    run_test()
