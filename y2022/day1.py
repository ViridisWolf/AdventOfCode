#!/usr/bin/env python

from AdventOfCode import read_data


def day(lines):
    current = 0
    elves = []
    for line in lines + ['']:
        if not line:
            elves.append(current)
            current = 0
            continue
        current += int(line)

    elves.sort()
    # print(f"Answer for 2022 day 1 part 1: {elves[-1]}")
    # print(f"Answer for 2022 day 1 part 2: {sum(elves[-3:])}")
    return elves[-1], sum(elves[-3:])


def main():
    lines = read_data(__file__)
    return day(lines)


expected_answers = 69912, 208180
