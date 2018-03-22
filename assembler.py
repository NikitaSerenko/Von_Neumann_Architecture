import numpy as np

from x86.memory import *

class Assembler:
    def __init__(self, _input_file):
        self.offset = 0
        self.command = np.array([], dtype=np.int64)
        self.static_data = np.array([], dtype=np.int64)
        self.input_file = _input_file
        self.idx_func = 0
        self.funcs = {}

    def translate_in_memory(self, _output_file):
        with open(self.input_file, 'r') as file:
            for line in file:
                command_line = np.array(self.to_memory(line), dtype=np.int64)
                self.append_command(command_line)

        self.command = np.array([len(self.command) + 1] +
                                        list(self.command) + 
                                        list(self.static_data))
        self.save_to(_output_file)

    def save_to(self, file_name):
        self.command.tofile(file_name)

    def add(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        s_lvl, s_arg = self.interpret(tokens[2])
        return KEY_ADD, f_lvl, f_arg, s_lvl, s_arg

    def call(self, tokens):
        idx = self.funcs[tokens[1]]
        return KEY_CALL, 0, idx, 0, 0

    def input(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        return KEY_INPUT, f_lvl, f_arg, 0, 0

    def dec(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        return KEY_DEC, f_lvl, f_arg, 0, 0

    def func_begin(self, tokens):
        if (tokens[1] not in self.funcs):
            self.funcs[tokens[1]] = self.idx_func
            self.idx_func += 1
        idx = self.funcs[tokens[1]]
        return KEY_FUNC_BEGIN, 0, idx, 0, 0

    def func_end(self):
        return KEY_FUNC_END, 0, 0, 0, 0

    def jump(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        s_lvl, s_arg = self.interpret(tokens[2])
        return KEY_JUMP, f_lvl, f_arg, s_lvl, s_arg

    def move(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        s_lvl, s_arg = self.interpret(tokens[2])
        return KEY_MOVE, f_lvl, f_arg, s_lvl, s_arg

    def pop(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        return KEY_POP, f_lvl, f_arg, 0, 0

    def push(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        return KEY_PUSH, f_lvl, f_arg, 0, 0

    def exit(self):
        return KEY_EXIT, 0, 0, 0, 0

    def out(self, tokens):
        f_lvl, f_arg = self.interpret(tokens[1])
        return KEY_OUT, f_lvl, f_arg, 0, 0

    def put_str(self, line):
        tokens = line.split(maxsplit=1)[1].strip()
        encoded_text = np.array([ord(el) for el in tokens], dtype=np.int64)
        self.offset += len(tokens)
        self.append_static(encoded_text)
        return KEY_STRING, self.offset - len(tokens), len(tokens), 0, 0

    def append_command(self, command_line):
        self.command = np.append(self.command, command_line)

    def append_static(self, static_data):
        self.static_data = np.append(self.static_data, static_data)

    def to_memory(self, line):
        tokens = line.split()
        if tokens[0] == NAME_ADD:
            return self.add(tokens)
        elif tokens[0] == NAME_EXIT:
            return self.exit()
        elif tokens[0] == NAME_FUNC_BEGIN:
            return self.func_begin(tokens)
        elif tokens[0] == NAME_FUNC_END:
            return self.func_end()
        elif tokens[0] == NAME_CALL:
            return self.call(tokens)
        elif tokens[0] == NAME_JUMP:
            return self.jump(tokens)
        elif tokens[0] == NAME_MOVE:
            return self.move(tokens)
        elif tokens[0] == NAME_POP:
            return self.pop(tokens)
        elif tokens[0] == NAME_STRING:
            return self.put_str(line)
        elif tokens[0] == NAME_INPUT:
            return self.input(tokens)
        elif tokens[0] == NAME_DEC:
            return self.dec(tokens)
        elif tokens[0] == NAME_OUT:
            return self.out(tokens)
        elif tokens[0] == NAME_PUSH:
            return self.push(tokens)

    def interpret(self, token):
        lvl = 0
        for i in token:
            if i == '*':
                lvl += 1
            else:
                arg = token[lvl:]
                if arg.isdigit():
                    arg = int(arg)
                else:
                    arg = REGISTERS_BY_NAME[arg]
                return lvl, arg

if __name__ == '__main__':
    input_file, output_file = 'fib.asm', 'binary_file'
    assembler = Assembler(input_file)
    assembler.translate_in_memory(output_file)
