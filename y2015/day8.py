#!/usr/bin/env python

import re

from AdventOfCode import read_data


def part1_v1(data):
    """ Count how many characters are needed to represent the input data in code and in-memory. """
    code_count = 0
    literal_count = 0
    for line in data:
        code_count += len(line)

        line = line[1:-1]
        line = re.sub(r'\\(\\|"|x..)', '?', line)
        literal_count += len(line)

    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {code_count - literal_count}")


def part1_v3(data):
    """ Count how many characters are needed to represent the input data in code and in-memory. """
    # v3 is faster than v1 because it avoids regex and also replaces some string modification with string counting.
    code_count = 0
    literal_count = 0
    for line in data:
        code_count += len(line)

        # Remove instances of \\ from the string because they could be double counted.
        # For example, \\x would be counted for both \\ and \x.
        line = line.replace(r'\\', '?')
        literal_count += len(line) - line.count(r'\"') - (line.count(r'\x')*3) - 2

    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {code_count - literal_count}")


def part2(data):
    """ Count how many characters are needed to encode the input data. """
    code_count = 0
    encoded_count = 0
    for line in data:
        code_count += len(line)
        encoded_count += len(line) + line.count('"') + line.count("\\") + 2

    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {encoded_count - code_count}")


def main():
    data = read_data(__file__)
    part1_v3(data)
    part2(data)
