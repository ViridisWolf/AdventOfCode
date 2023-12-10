#!/usr/bin/env python
from AdventOfCode import read_data


class ComDev:
    opcode_times = {
        'noop': 1,
        'addx': 2,
    }

    def __init__(self, code):
        self.cycle = 1

        # CPU variables.
        self.x = 1
        self.ip = 0
        self.code = code
        self.current_instruction = code[0]
        self.remaining_cycles = self.opcode_times[self.current_instruction[0]] - 1

        # Screen variables.
        self.screen = [[]]
        self.screen_width = 40
        self.screen_height = 6

    def advance_cycle(self):
        self.update_screen()
        self.step_cpu()
        self.cycle += 1
        return self.ip < len(self.code)

    def update_screen(self):
        ray = self.cycle - 1
        column = ray % self.screen_width

        if len(self.screen[-1]) == self.screen_width:
            self.screen.append([])
        if abs(column - self.x) <= 1:
            self.screen[-1].append('█')
        else:
            self.screen[-1].append(' ')

        # print(f"\ncol: {column}, x: {self.x}, delta {abs(column - self.x)}")
        # self.print_screen()

    def get_screen(self):
        return '\n'.join([''.join(row) for row in self.screen])

    def step_cpu(self):
        # print(f"Cycle: {self.cycle}, x: {self.x}, signal: {self.get_signal_strength()}, in-progress: {self.current_instruction}")
        if self.remaining_cycles:
            self.remaining_cycles -= 1
        else:
            instruction = self.current_instruction
            if instruction[0] == "noop":
                pass
            elif instruction[0] == "addx":
                self.x += int(instruction[1])
            else:
                raise AssertionError

            self.ip += 1
            if self.ip < len(self.code):
                self.current_instruction = self.code[self.ip]
                self.remaining_cycles = self.opcode_times[self.current_instruction[0]] - 1
            else:
                assert self.ip == len(self.code)
                # Don't fetch an instruction on the last iteration.

    def get_signal_strength(self):
        return self.cycle * self.x


def day(data):
    code = []
    for line in data:
        code.append(line.split(' '))

    device = ComDev(code)
    total_signal = 0
    while device.advance_cycle():
        if device.cycle in [20, 60, 100, 140, 180, 220]:
            # print(f"cycle {device.cycle} signal: {device.get_signal_strength()}")
            total_signal += device.get_signal_strength()

    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {total_signal}")
    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2:\n{device.get_screen()}")
    return total_signal, device.get_screen()


def main():
    data = read_data()
    return day(data)


expected_answers = 12880, ("████  ██    ██  ██  ███    ██ ███  ████ \n"
                           "█    █  █    █ █  █ █  █    █ █  █ █    \n"
                           "███  █       █ █  █ █  █    █ █  █ ███  \n"
                           "█    █       █ ████ ███     █ ███  █    \n"
                           "█    █  █ █  █ █  █ █    █  █ █ █  █    \n"
                           "█     ██   ██  █  █ █     ██  █  █ ████ ")
