NO_ERROR = True


class Operation(object):
    def __init__(self, obj_code, i_format):
        self.obj_code = obj_code
        self.format = i_format


class BaseReg(object):
    BaseValue = 51
    BaseFlag = False
    __UnOfficialValue = 0

    @staticmethod
    def check_ldb(instruction):
        if instruction.operation.casefold() == "LDB".casefold():
            if instruction.operand.isdigit():
                BaseReg.__UnOfficialValue = int(instruction.operand)
            else:
                BaseReg.__UnOfficialValue = int(SymbolTable.get(instruction.operand), 16)

    @staticmethod
    def setBaseValue():
        BaseReg.BaseValue = BaseReg.__UnOfficialValue


class AddressingModes(object):
    IMMEDIATE = 0b010000
    INDIRECT = 0b100000
    DIRECT = 0b110000

    PC_RELATIVE = 0b000010
    BASE_RELATIVE = 0b000100

    INDEXED = 0b001000
    EXTENDED = 0b000001


OPTAB = {"ADD": "18",
         "AND": "40",
         "COMP": "28",
         "DIV": "24",
         "J": "3C",
         "JEQ": "30",
         "JGT": "34",
         "JLT": "38",
         "JSUB": "48",
         "LDA": "00",
         "LDCH": "50",
         "LDL": "08",
         "LDX": "04",
         "MUL": "20",
         "OR": "44",
         "RD": "D8",
         "RSUB": "4C",
         "STA": "0C",
         "STCH": "54",
         "STL": "14",
         "STSW": "E8",
         "STX": "10",
         "SUB": "1C",
         "TD": "E0",
         "TIX": "2C",
         "WD": "DC"}

OperationTable = {
    "ADD": Operation("18", 3),
    "ADDF": Operation("58", 3),
    "ADDR": Operation("90", 2),
    "AND": Operation("40", 3),
    "CLEAR": Operation("B4", 2),
    "COMP": Operation("28", 3),
    "COMPF": Operation("88", 3),
    "COMPR": Operation("A0", 2),
    "DIV": Operation("24", 3),
    "DIVF": Operation("64", 3),
    "DIVR": Operation("9C", 2),
    "FIX": Operation("C4", 1),
    "FLOAT": Operation("C0", 1),
    "HIO": Operation("F4", 1),
    "J": Operation("3C", 3),
    "JEQ": Operation("30", 3),
    "JGT": Operation("34", 3),
    "JLT": Operation("38", 3),
    "JSUB": Operation("48", 3),
    "LDA": Operation("00", 3),
    "LDB": Operation("68", 3),
    "LDCH": Operation("50", 3),
    "LDF": Operation("70", 3),
    "LDL": Operation("08", 3),
    "LDX": Operation("04", 3),
    "LDS": Operation("6C", 3),
    "LDT": Operation("74", 3),
    "MUL": Operation("20", 3),
    "OR": Operation("44", 3),
    "RD": Operation("D8", 3),
    "RSUB": Operation("4C", 3),
    "STA": Operation("0C", 3),
    "STCH": Operation("54", 3),
    "STL": Operation("14", 3),
    "STSW": Operation("E8", 3),
    "STX": Operation("10", 3),
    "SUB": Operation("1C", 3),
    "TD": Operation("E0", 3),
    "TIX": Operation("2C", 3),
    "TIXR": Operation("B8", 2),
    "WD": Operation("DC", 3)
}

RegisterTable = {
    "A": 0,
    "X": 1,
    "L": 2,
    "B": 3,
    "S": 4,
    "T": 5,
    "F": 6
}

SymbolTable = {}
