#!/usr/bin/env python

from AdventOfCode import read_data


def part1(lines):
    """ Calculate final floor, assuming '(' means up one and ')' means down one. """
    data = lines[0]
    return data.count('(') - data.count(')')


def part2(lines):
    """ Calculate the first character which causes Santa to enter the basement. """
    floor = 0
    for index, char in enumerate(lines[0]):
        if char == '(':
            floor += 1
        else:
            floor -= 1
        if floor < 0:
            return index + 1


def main():
    data = read_data()
    return part1(data), part2(data)


expected_answers = (138, 1771)
