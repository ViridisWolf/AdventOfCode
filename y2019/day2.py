#!/usr/bin/env python

from AdventOfCode import read_data


class IntcodeComputer:
    class ops:
        add = object()
        mult = object()
        halt = object()

    op_from_code = {
            1: ops.add,
            2: ops.mult,
            99: ops.halt,
            }
    opcode = {v: k for k, v in op_from_code.items()}

    def __init__(self, data_str):
        self.instruction_pointer = 0
        self.data = [int(x) for x in data_str.split(',')]

    def read_mem(self, position):
        assert position >= 0
        if position >= len(self.data):
            return None
        return self.data[position]

    def step(self):
        op = self.data[self.instruction_pointer]
        op = self.op_from_code.get(op, op)
        arg1 = self.read_mem(self.instruction_pointer + 1)
        arg2 = self.read_mem(self.instruction_pointer + 2)
        arg3 = self.read_mem(self.instruction_pointer + 3)

        #print(f"Instruction at {}: {}, {}, {}, {}".format(
        #        self.instruction_pointer,
        #        self.data[self.instruction_pointer],
        #        arg1, arg2, arg3
        #        ))

        if op is self.ops.add:
            # Add data at arg1 and arg2, store at arg3.
            self.data[arg3] = self.read_mem(arg1) + self.read_mem(arg2)
        elif op is self.ops.mult:
            # Multiply the data at arg1 and arg2, store at arg3.
            self.data[arg3] = self.read_mem(arg1) * self.read_mem(arg2)
        elif op is self.ops.halt:
            # Do nothing except return.  Do not advance the instruction pointer.
            return
        else:
            raise AssertionError(f"Unknown opcode: {op}")

        # Advance the instruction pointer to the position of the next instruction.
        # Every instruction is 4 positions in size.
        self.instruction_pointer += 4

    def run(self):
        while self.data[self.instruction_pointer] != self.opcode[self.ops.halt]:
            self.step()


def part1():
    computer = IntcodeComputer(read_data()[0])
    computer.data[1] = 12
    computer.data[2] = 2
    computer.run()
    answer = computer.data[0]
    # print(f"Answer for 2019 day 2 part 1: {answer}")
    return answer


def part2():
    line = read_data()[0]
    noun = -1
    output = None
    while output != 19690720:
        noun += 1
        for verb in range(0, 99):
            computer = IntcodeComputer(line)
            computer.data[1] = noun
            computer.data[2] = verb
            computer.run()
            output = computer.data[0]
            # print(f"noun={noun} and verb={verb} resulted in output={output:0, d}.")
            if output == 19690720:
                break

    if output != 19690720:
        raise AssertionError("Did not find the answer!")
    # print(f"Answer for 2019 day 2 part 2: {100*noun + verb}")
    return 100*noun + verb


def main():
    answer1 = part1()
    answer2 = part2()
    return answer1, answer2


expected_answers = 9706670, 2552
