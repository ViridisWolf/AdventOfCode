#!/usr/bin/env python

from AdventOfCode import read_data


def get_adjacent_points(cube):
    x, y, z = cube
    return [(x - 1, y, z), (x + 1, y, z),
            (x, y - 1, z), (x, y + 1, z),
            (x, y, z - 1), (x, y, z + 1)]


def get_adjacent_cube_counts(cube, cubes):
    adjacent_count = 0
    for adjacent in get_adjacent_points(cube):
        if adjacent in cubes:
            adjacent_count += 1
    return adjacent_count


def part1(data):
    """ How many sides of the cubes (puzzle input) are not touching another cube?"""
    cubes = set()
    for line in data:
        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)
        cubes.add((x, y, z))

    exposed_sides = 0
    for cube in cubes:
        exposed_sides += 6 - get_adjacent_cube_counts(cube, cubes)
    return exposed_sides


# Part 2 functions.
def fill_outside(cubes, max_dimensions):
    """ Return a set of points which are outside the specified cubes. """
    outside = set()
    mx, my, mz = max_dimensions
    count = 0

    changing = True
    while changing:
        changing = False
        count += 1
        for z in range(-1, mz + 2):
            for y in range(-1, my + 2):
                for x in range(-1, mx + 2):
                    point = x, y, z
                    if not ((0 <= x <= mx) and (0 <= y <= my) and (0 <= z <= mz)):
                        # Outside all the lava cubes.
                        outside.add(point)
                        continue
                    if point in cubes or point in outside:
                        continue
                    if any(adjacent in outside for adjacent in get_adjacent_points(point)):
                        outside.add(point)
                        changing = True

    return outside


def part2(data):
    """ How many sides of the cubes (puzzle input) are exposed to the outside? """
    cubes = set()
    max_dimensions = [0, 0, 0]
    for line in data:
        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)
        cubes.add((x, y, z))
        max_dimensions[0] = max(max_dimensions[0], x)
        max_dimensions[1] = max(max_dimensions[1], y)
        max_dimensions[2] = max(max_dimensions[2], z)
        assert x >= 0 and y >= 0 and z >= 0

    outside = fill_outside(cubes, max_dimensions)

    exposed_sides = 0
    for cube in cubes:
        exposed_sides += get_adjacent_cube_counts(cube, outside)
    return exposed_sides


def main():
    data = read_data(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2


expected_answers = 4282, 2452
