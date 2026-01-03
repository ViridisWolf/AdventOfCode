#!/usr/bin/env python
from AdventOfCode import read_data


def part1(lines):
    """
    This is supposed to be about checking to see if the specified number of shapes can be fit in
    the given region area.  However, that would be extremely slow, and the puzzle input is such
    that we can just check the extreme upper and lower bounds of how much space the shapes need.

    This does not work for the example puzzle input; only the real puzzle input.
    """
    possible_count = 0
    # shapes = []
    for index, line in enumerate(lines):
        if 'x' in line:
            break
        # elif line.endswith(':'):
        #     shapes.append(0)
        # elif '#' in line:
        #     shapes[-1] += line.count('#')

    for line in lines[index:]:
        space, counts = line.split(':')
        size = int(space.split('x')[0]) * int(space.split('x')[1])
        requirements = [int(x) for x in counts.split()]
        # min_needed = sum([shapes[index]*req for index, req in enumerate(requirements)])
        max_needed = 9*sum(requirements)  # Each shape fits in a 3x3 square.
        if size >= max_needed:
            possible_count += 1
        # else:
        #     assert size < min_needed

    return possible_count


def main():
    lines = read_data()
    return part1(lines), None


expected_answers = 427, None
