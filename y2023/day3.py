#!/usr/bin/env python
import math
import re

from AdventOfCode import read_data


def adjacency(part, loc, schematic):
    """
    Find adjacent symbols and gears.

    :param part: The number as a string.
    :param loc: The starting (left-most) location of the number.
    :param schematic: The puzzle schematic of numbers and symbols in dictionary form.
    :return: Tuple of boolean of any symbol being present and list of gears.
    """
    x, y = loc
    any_symbol = False
    gears = []

    assert len(part) <= 3
    if len(part) == 3:
        deltas = [
            (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
            (-1,  0),                            (3,  0),
            (-1,  1), (0,  1), (1,  1), (2,  1), (3,  1),
        ]
    elif len(part) == 2:
        deltas = [
            (-1, -1), (0, -1), (1, -1), (2, -1),
            (-1,  0),                   (2,  0),
            (-1,  1), (0,  1), (1,  1), (2,  1),
        ]
    else:
        deltas = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1),
        ]

    for dx, dy in deltas:
        new_x = x + dx
        new_y = y + dy
        neighbor = schematic.get((new_x, new_y), '.')
        if neighbor != '.':
            # This assert is not valid for how the puzzle is worded, but it is valid for the actual puzzle
            # inputs, and it helped to find a code bug.
            # assert not schematic.get((new_x, new_y), '.').isdigit()
            any_symbol = True
            if neighbor == '*':
                gears.append((new_x, new_y))

    return any_symbol, gears


def both_parts(data):
    """
    Part 1: Find the part numbers in the schematic (puzzle input), which are any number which is adjacent to a symbol.
            Then calculate the sum of those numbers as the answer.
    Part 2: Find gears ('*') with two adjacent numbers, and calculate the gear's ratio as the product of those two
            numbers.  Sum these ratios as the answer.
    """

    # First create a dictionary form of the schematic.
    schematic = {}
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char != '.':
                schematic[(col, row)] = char

    # Walk over the schematic lines to find the numbers and then what they are adjacent to.
    part_sum = 0
    gears = {}
    for y, line in enumerate(data):
        for match in re.finditer(r'\d\d?\d?', line):
            x = match.start(0)
            part = match.group(0)
            is_part, adjacent_gears = adjacency(part, (x, y), schematic)
            if is_part:
                part_sum += int(part)
            for gear in adjacent_gears:
                if gear not in gears:
                    gears[gear] = set()
                gears[gear].add(int(part))

    ratio_sum = 0
    for gear, parts in gears.items():
        if len(parts) == 2:
            ratio = math.prod(parts)
            ratio_sum += ratio

    return part_sum, ratio_sum


def main():
    data = read_data()
    return both_parts(data)


expected_answers = 553079, 84363105
