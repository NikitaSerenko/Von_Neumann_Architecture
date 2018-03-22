import numpy

from x86.memory import *


class Disassembler:
    def __init__(self, _input_file):
        self.input_file = _input_file
        self.offset = 0
        self.func_index = 0
        self.known_funcs = dict()

    def get_func_name(self, identifier):
        if identifier in self.known_funcs:
            return self.known_funcs[identifier]
        else:
            self.func_index += 1
            self.known_funcs[identifier] = f'FUNC_{self.func_index}'
            return f'FUNC_{self.func_index}'

    def define(self, lvl, arg):
        if lvl == 0:
            return ' ' + str(arg)
        else:
            return ' ' + '*' * lvl + REGISTERS_BY_KEY[arg]

    def add(self, f_lvl, f_arg, s_lvl, s_arg):
        return NAME_ADD + self.define(f_lvl, f_arg) + self.define(s_lvl, s_arg)

    def call(self, f_arg):
        return NAME_CALL + ' ' + self.get_func_name(f_arg)

    def exit(self):
        return NAME_EXIT

    def put_str(self, data, f_lvl, f_arg):
        return NAME_STRING + ' ' + ''.join([chr(data[self.offset + f_lvl + i]) for i in range(f_arg)])

    def input(self, f_lvl, f_arg):
        return NAME_INPUT + self.define(f_lvl, f_arg)

    def dec(self, f_lvl, f_arg, s_lvl, s_arg):
        return NAME_DEC + self.define(f_lvl, f_arg)

    def func_begin(self, f_arg):
        return NAME_FUNC_BEGIN + ' ' + self.get_func_name(f_arg)

    def func_end(self):
        return NAME_FUNC_END

    def jump(self, f_lvl, f_arg, s_arg):
        return NAME_JUMP + ' ' + '*' * f_lvl + REGISTERS_BY_KEY[f_arg] + ' ' + str(s_arg)

    def mov(self, f_lvl, f_arg, s_lvl, s_arg):
        return NAME_MOVE + self.define(f_lvl, f_arg) + self.define(s_lvl, s_arg)

    def pop(self, f_lvl, f_arg):
        return NAME_POP + self.define(f_lvl, f_arg)

    def print(self, f_lvl, f_arg):
        return NAME_OUT + self.define(f_lvl, f_arg)

    def push(self, f_lvl, f_arg):
        return NAME_PUSH + self.define(f_lvl, f_arg)

    def from_memory(self, data, command, f_lvl, f_arg, s_lvl, s_arg):
        if command == KEY_ADD:
            return self.add(f_lvl, f_arg, s_lvl, s_arg)
        elif command == KEY_CALL:
            return self.call(f_arg)
        elif command == KEY_EXIT:
            return self.exit()
        elif command == KEY_FUNC_BEGIN:
            return self.func_begin(f_arg)
        elif command == KEY_FUNC_END:
            return self.func_end()
        elif command == KEY_JUMP:
            return self.jump(f_lvl, f_arg, s_arg)
        elif command == KEY_MOVE:
            return self.mov(f_lvl, f_arg, s_lvl, s_arg)
        elif command == KEY_POP:
            return self.pop(f_lvl, f_arg)
        elif command == KEY_OUT:
            return self.print(f_lvl, f_arg)
        elif command == KEY_PUSH:
            return self.push(f_lvl, f_arg)
        elif command == KEY_STRING:
            return self.put_str(data, f_lvl, f_arg)
        elif command == KEY_INPUT:
            return self.input(f_lvl, f_arg)
        elif command == KEY_DEC:
            return self.dec(f_lvl, f_arg, s_lvl, s_arg)
        raise KeyError

    def to_file(self, _output_file):
        data = numpy.fromfile(self.input_file, dtype=numpy.int64)
        with open(output_file, 'w') as output:
            self.offset = data[0]
            length = int((self.offset - 1) / STEP)
            source_text = ''
            for i in range(length):
                code, f_lvl, f_arg, s_lvl, s_arg = data[STEP * i + 1: STEP * i + 6]
                source_text += self.from_memory(data, code, f_lvl, f_arg, s_lvl, s_arg) + '\n'
            output.write(source_text)


if __name__ == '__main__':
    input_file = 'binary_file'
    output_file = 'disassembled.asm'
    disassembler = Disassembler(input_file)
    disassembler.to_file(output_file)
