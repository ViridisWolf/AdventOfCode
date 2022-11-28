#!/usr/bin/env python3

from AdventOfCode import read_data


def part1():
    houses = {(0, 0): 1}
    # Up is +y, right is +x.
    x, y = 0, 0

    lines = read_data(__file__)
    for line in lines:
        for char in line:
            if char == 'v':
                y -= 1
            elif char == '<':
                x -= 1
            elif char == '^':
                y += 1
            elif char == '>':
                x += 1
            else:
                raise AssertionError

            houses[(x, y)] = houses.get((x, y), 0) + 1

    print(f"Answer for 2015 day 3 part 1: {len(houses)}")


def part2():
    houses = {(0, 0): 2}
    # Up is +y, right is +x.
    location = {0: [0, 0],
                1: [0, 0]}
    turn = 0

    lines = read_data(__file__)
    for line in lines:
        for char in line:
            if char == 'v':
                location[turn][1] -= 1
            elif char == '<':
                location[turn][0] -= 1
            elif char == '^':
                location[turn][1] += 1
            elif char == '>':
                location[turn][0] += 1
            else:
                raise AssertionError
            turn ^= 1
            houses[tuple(location[turn])] = houses.get(tuple(location[turn]), 0) + 1

    print(f"Answer for 2015 day 3 part 2: {len(houses)}")


def main():
    part1()
    part2()
