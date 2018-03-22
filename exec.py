import numpy

from x86.memory import *


class VMachine:
    def __init__(self, memory):
        self.memory = memory
        self.in_func = False
        self.func_start = {}

    def mvIp(self):
        self.memory.write(IP_INDEX, self.gIp() + STEP)

    def gIp(self):
        return self.memory.read(IP_INDEX)

    def gSp(self):
        return self.memory.read(SP_INDEX)

    def at_adress(self, lvl, data):
        for _ in range(lvl):
            data = self.memory.read(data)
        return data

    def add(self, f_lvl, f_arg, s_lvl, s_arg):
        data = self.at_adress(f_lvl, f_arg) + self.at_adress(s_lvl, s_arg)
        self.memory.write(self.at_adress(f_lvl - 1, f_arg), data)

    def call(self, f_arg):
        self.push(0, self.gIp())
        self.move(1, IP_INDEX, 0, self.func_start[f_arg])

    def jump(self, f_lvl, f_arg, s_lvl, s_arg):
        if self.at_adress(f_lvl, f_arg) != s_lvl:
            self.add(1, IP_INDEX, 0, (s_arg - 1) * STEP)

    def move(self, f_lvl, f_arg, s_lvl, s_arg):
        data = self.at_adress(s_lvl, s_arg)
        self.memory.write(self.at_adress(f_lvl - 1, f_arg), data)

    def pop(self, f_lvl, f_arg):
        data = self.at_adress(2, SP_INDEX)
        self.memory.write(self.at_adress(f_lvl - 1, f_arg), data)
        self.memory.write(self.gSp(), 0)
        self.add(1, SP_INDEX, 0, 1)

    def func_begin(self, f_arg):
        self.in_func = True
        self.func_start[f_arg] = self.gIp()

    def func_end(self):
        self.in_func = False

    def out(self, f_lvl, f_arg):
        print(self.at_adress(f_lvl, f_arg))

    def push(self, f_lvl, f_arg):
        self.dec(1, SP_INDEX)
        self.move(2, SP_INDEX, f_lvl, f_arg)

    def put_str(self, f_lvl, f_arg):
        print(''.join([chr(self.memory.read(REGISTERS_COUNT + self.memory.offset + f_lvl + i)) for i in range(f_arg)]))

    def input(self, f_lvl, f_arg):
        self.memory.write(self.at_adress(f_lvl - 1, f_arg), input())

    def dec(self, f_lvl, f_arg):
        data = self.at_adress(f_lvl, f_arg) - 1
        self.memory.write(self.at_adress(f_lvl - 1, f_arg), data)

    def exec(self, command, f_lvl, f_arg, s_lvl, s_arg):
        if command == KEY_EXIT:
            return False
        self.mvIp()

        if self.in_func and command != KEY_FUNC_END:
            pass
        elif command == KEY_ADD:
            self.add(f_lvl, f_arg, s_lvl, s_arg)
        elif command == KEY_CALL:
            self.call(f_arg)
        elif command == KEY_FUNC_BEGIN:
            self.func_begin(f_arg)
        elif command == KEY_FUNC_END:
            self.func_end()
        elif command == KEY_JUMP:
            self.jump(f_lvl, f_arg, s_lvl, s_arg)
        elif command == KEY_MOVE:
            self.move(f_lvl, f_arg, s_lvl, s_arg)
        elif command == KEY_POP:
            self.pop(f_lvl, f_arg)
        elif command == KEY_OUT:
            self.out(f_lvl, f_arg)
        elif command == KEY_PUSH:
            self.push(f_lvl, f_arg)
        elif command == KEY_STRING:
            self.put_str(f_lvl, f_arg)
        elif command == KEY_INPUT:
            self.input(f_lvl, f_arg)
        elif command == KEY_DEC:
            self.dec(f_lvl, f_arg)
        else:
            return False
        return True

    def gCommand(self):
        key = self.memory.read(self.gIp())
        f_lvl = self.memory.read(self.gIp() + 1)
        f_arg = self.memory.read(self.gIp() + 2)
        s_lvl = self.memory.read(self.gIp() + 3)
        s_arg = self.memory.read(self.gIp() + 4)
        return self.exec(key, f_lvl, f_arg, s_lvl, s_arg)

    def run(self):
        while self.gCommand():
            pass


if __name__ == '__main__':
    input_file = 'binary_file'
    vMachine = VMachine(Memory.from_file(input_file))
    vMachine.run()
