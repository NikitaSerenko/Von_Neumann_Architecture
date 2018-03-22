import numpy

IP_INDEX = 0
SP_INDEX = 1

MEMORY_SIZE = 1024
STEP = 5

REGISTERS_COUNT = 8

REGISTERS_BY_NAME = {
    'IP': 0,
    'SP': 1,
    'EAX': 2,
    'EBX': 3,
    'ECX': 4,
    'EDX': 5,
    'EEX': 6,
    'EFX': 7
}

REGISTERS_BY_KEY = {
    0: 'IP',
    1: 'SP',
    2: 'EAX',
    3: 'EBX',
    4: 'ECX',
    5: 'EDX',
    6: 'EEX',
    7: 'EFX'
}

KEY_ADD = 0
KEY_CALL = 1
KEY_EXIT = 2
KEY_FUNC_BEGIN = 3
KEY_FUNC_END = 4
KEY_JUMP = 5
KEY_MOVE = 6
KEY_POP = 7
KEY_OUT = 8
KEY_PUSH = 9
KEY_STRING = 10
KEY_INPUT = 11
KEY_DEC = 12

NAME_ADD = 'ADD'
NAME_CALL = 'CALL'
NAME_EXIT = 'EXIT'
NAME_FUNC_BEGIN = 'FUNC_BEGIN'
NAME_FUNC_END = 'FUNC_END'
NAME_JUMP = 'GO_TO'
NAME_MOVE = 'MOV'
NAME_POP = 'POP'
NAME_OUT = 'OUT'
NAME_PUSH = 'PUSH'
NAME_STRING = 'STRING'
NAME_INPUT = 'INPUT'
NAME_DEC = 'DEC'


class Memory:
    def __init__(self, size=MEMORY_SIZE):
        self.memory = numpy.zeros(size, dtype=numpy.int64)
        self.offset = 0

    def read(self, address):
        return self.memory[address]

    def write(self, address, data):
        self.memory[address] = data

    @classmethod
    def from_file(cls, file_name):
        mem = cls()
        mem.write(IP_INDEX, REGISTERS_COUNT + 1)
        mem.write(SP_INDEX, MEMORY_SIZE)
        byte_code = numpy.fromfile(file_name, dtype=numpy.int64)
        for i, byte in enumerate(byte_code):
            mem.write(REGISTERS_COUNT + i, byte)
        mem.offset = byte_code[0]
        return mem

