from SIC_XE.SIC_XE_Data import AddressingModes


class Instruction(object):
    def __init__(self, label, operation, operand):
        self.label = label
        self.operation = operation
        self.operand = operand
        self.addressing_mode = 0b000000
        self.address = None
        self.obj_code = None
        self.error = False
        self.length = 0

    def check_addressing_mode(self):
        nixbpe = 0b000000
        if self.operation[0].casefold() == "+".casefold():
            nixbpe |= AddressingModes.EXTENDED
            self.operation = self.operation[1:]
        if self.operand is None:
            return
        if self.operand[0].casefold() == "#".casefold():
            nixbpe |= AddressingModes.IMMEDIATE
            self.operand = self.operand[1:]
        elif self.operand[0].casefold() == "@".casefold():
            nixbpe |= AddressingModes.INDIRECT
            self.operand = self.operand[1:]
        else:
            nixbpe |= AddressingModes.DIRECT
            if self.operand[-2:].casefold() == ",X".casefold():  # no need to check for length as we use ':'
                nixbpe |= AddressingModes.INDEXED
                self.operand = self.operand[:-2]
        self.addressing_mode = nixbpe

    def get_word_operand(self):
        return format(int(self.operand), '06X')

    def get_byte_operand(self):
        first_letter = self.operand[0].casefold()
        if first_letter == "C".casefold():
            return "".join([hex(ord(char))[2:] for char in self.operand[2:-1]]).upper()
        elif first_letter == "X".casefold():
            return self.operand[2:-1].upper()

    def __str__(self):
        return "{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(self.address,
                                                         self.label, self.operation, self.operand,
                                                         bin(self.addressing_mode), self.obj_code)

    def list_file_format(self):
        # Debuggnig :: the format of each parameter and add the error if exists
        return "{}\t{}\t{}\t{}\t{}".format(self.address, self.label, self.operation, self.operand, self.obj_code)
