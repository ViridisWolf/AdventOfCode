#!/usr/bin/env python

from AdventOfCode import read_data


class Program:
    def __init__(self, code):
        self.ip = 0
        self.accumulator = 0
        self.code = code
        self.terminated = None

    def step(self):
        opcode, value = self.code[self.ip]
        if opcode == 'acc':
            self.accumulator += value
        elif opcode == 'jmp':
            self.ip += value - 1
        elif opcode == 'nop':
            pass
        else:
            raise AssertionError
        self.ip += 1

    def run(self):
        """
        Run until a loop is detected or non-existent code is reached.

        self.terminated will be set to False if the program hit a loop, else True.
        """
        self.terminated = False
        ips_visited = set()
        while self.ip not in ips_visited:
            ips_visited.add(self.ip)
            self.step()
            if self.ip > len(self.code):
                continue
            elif self.ip == len(self.code):
                self.terminated = True
                break


def part1(code):
    state = Program(code)
    state.run()
    # print(f"Answer for 2020 day 8 part 1: {state.accumulator}")
    return state.accumulator


def part2(code):
    for ip in range(len(code)):
        opcode, arg = code[ip]
        if opcode == 'acc':
            continue
        alt_code = code[:]
        alt_code[ip] = ('nop' if opcode == 'jmp' else 'jmp'), arg

        state = Program(alt_code)
        state.run()
        if state.terminated:
            break
    # print(f"Answer for 2020 day 8 part 2: {state.accumulator}")
    return state.accumulator


def main():
    lines = read_data(__file__)
    code = []
    for line in lines:
        opcode, arg = line.split(' ')
        code.append((opcode, int(arg)))

    answer1 = part1(code)
    answer2 = part2(code)
    return answer1, answer2


expected_answers = 1610, 1703
