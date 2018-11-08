import warnings
from SIC_XE.SIC_XE_InstructionClass import Instruction

LitTab = {}


def create_literal_pool(current_address):
    last_address = current_address
    literal_instructions = []
    for value in LitTab:
        if LitTab[value].added_to_pool: continue
        LitTab[value].added_to_pool = True
        LitTab[value].address = last_address
        instr = Instruction('*', LitTab[value].name, None)
        instr.length = LitTab[value].length
        instr.obj_code = value
        instr.address = last_address
        literal_instructions.append(instr)
        last_address += instr.length
    return last_address, literal_instructions

# Debugging:: i can send the instruction itself and create the literal faster
def check_for_literal(instr_operand, pc_value):
    # check for literal in operand if so process it
    if instr_operand is not None and instr_operand.startswith('='):
        if instr_operand[1] == '*':
            Literal.process(instr_operand, pc_value)
        Literal.process(instr_operand)


class Literal(object):
    def __init__(self, name, value=None, length=None):
        if value is None or length is None:
            self.__old_constructor(name)
        else:
            self.name = name
            self.value = value
            self.length = length
            self.address = None
            self.added_to_pool = False

    @staticmethod
    def process(name, LocCTR=None):
        if LocCTR is not None:
            LitTab[LocCTR] = Literal(name, LocCTR, 3)
        else:
            x_or_c, value = Literal.__calc_value(name)
            if LitTab.get(value) is None:
                length = Literal.__calc_length(name, x_or_c)
                LitTab[value] = Literal(name, value, length)

    @staticmethod
    def __calc_value(name):
        second_letter = name[1].casefold()
        if second_letter == "C".casefold():
            return "C", "".join([hex(ord(char))[2:] for char in name[3:-1]]).upper()
        elif second_letter == "X".casefold():
            return "X", name[3:-1].upper()

    @staticmethod
    def __calc_length(name, x_or_c):
        length = len(name) - 4
        return round(length / 2) if x_or_c == "X" else length

    def __old_constructor(self, name):
        warnings.warn("deprecated ! don't use this ,, Use static method 'check_literal(literal_name)'",
                      DeprecationWarning)
        self.name = name
        self.length, self.value = self.__calc_length_value()
        self.address = None
        self.added_to_pool = False
        if LitTab.get(self.value) is None:
            LitTab[self.value] = self
        else:
            del self

    def __calc_length_value(self):
        warnings.warn("deprecated ! don't use this ,, Use static method 'check_literal(literal_name)'",
                      DeprecationWarning)
        second_letter = self.name[1].casefold()
        length = len(self.name) - 4
        if second_letter == "C".casefold():
            return length, "".join([hex(ord(char))[2:] for char in self.name[3:-1]]).upper()
        elif second_letter == "X".casefold():
            return round(length / 2), self.name[3:-1].upper()

    @staticmethod
    def get_address_from_table(literal_name):
        value = Literal.__calc_value(literal_name)[1]
        # no need to check as this function will be called on the literal pool
        # and any literal here must have been added before
        return str(LitTab[value].address)
