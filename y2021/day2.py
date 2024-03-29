#!/usr/bin/env python3

from AdventOfCode import read_data


def main():
    depth_1 = 0
    depth_2 = 0
    horz = 0
    aim = 0

    lines = read_data()

    for line in lines:
        line = line.strip()
        if 'forward ' in line:
            horz += int(line[8:])
            depth_2 += int(line[8:]) * aim
        elif 'down ' in line:
            aim += int(line[5:])
            depth_1 += int(line[5:])
        elif 'up ' in line:
            aim -= int(line[3:])
            depth_1 -= int(line[3:])
        else:
            raise AssertionError("Should not have gotten here.")

    # print(f"Answer for 2021 day 2 part 1: {depth_1 * horz}")
    # print(f"Answer for 2021 day 2 part 2: {depth_2 * horz}")
    answer1 = depth_1 * horz
    answer2 = depth_2 * horz
    return answer1, answer2


expected_answers = 1962940, 1813664422
