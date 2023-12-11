#!/usr/bin/env python
import itertools

from AdventOfCode import read_data


def manhattan_distance(pair):
    """ Return the manhattan distance between the two points in 'pair'. """
    loc1, loc2 = pair
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x2 - x1) + abs(y2 - y1)


def both(data, expansion_ratio):
    """
    The puzzle input is an image of galaxies, but some of the space between galaxies needs expansion (due to expansion
    of the universe over time).  Any full row or column that doesn't have any galaxies in it needs expansion.

    Part 1: Each empty row or column gets replaced with two.
    Part 2: Each empty row or column gets replaced with 1 million.

    :param data: The puzzle input as a list of strings.
    :param expansion_ratio: The expansion ratio for empty rows/columns.
    :return: The sum of distances between each galaxy in the expanded image.
    """

    # This solution was inspired by Max's description of his solution.

    skips_x = []
    skips_y = []
    galaxies = []

    # Record how many skips/blanks/expansions there have been prior to each row.
    skips = 0
    for y, line in enumerate(data):
        if line == '.'*len(data[0]):
            skips += 1
        skips_y.append(skips)

    # Now record the number of skips in each column.
    skips = 0
    for x in range(len(data[0])):
        col = [row[x] == '.' for row in data]
        if all(col):
            skips += 1
        skips_x.append(skips)

    # Create a list of galaxies, and offset their location by the skip amount.
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                location = x + skips_x[x]*(expansion_ratio - 1), y + skips_y[y]*(expansion_ratio - 1)
                galaxies.append(location)

    # Add up all the distances between each galaxy.
    distances_sum = 0
    for pair in itertools.combinations(galaxies, 2):
        distances_sum += manhattan_distance(pair)
    return distances_sum


def main():
    data = read_data()
    answer1 = both(data, expansion_ratio=2)
    answer2 = both(data, expansion_ratio=1_000_000)
    return answer1, answer2


expected_answers = 10490062, 382979724122


# Below are what I had originally when I submitted my answers.
def manhattan_distance_orig(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x2 - x1) + abs(y2 - y1)


def display_dict(galaxies, max_x, max_y):
    g = 1
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in galaxies:
                print(g, end='')
                g += 1
            else:
                print('.', end='')
        print()


def display_list(galaxies):
    g = 1
    for row in galaxies:
        for x in row:
            if x == '#':
                print(g, end='')
                g += 1
            else:
                print('.', end='')
        print()


def part1_orig(data):
    image = []
    for line in data:
        if all([x == '.' for x in line]):
            image.append(line)
        image.append(line)

    col = 0
    while col < (len(image[0])) and col < len(2 * data[0]):
        empty = True
        for row in image:
            if row[col] != '.':
                empty = False
                break
        if empty:
            for index, row in enumerate(image):
                image[index] = row[:col] + '.' + row[col:]
            col += 1
        col += 1

    galaxies = []
    for y, row in enumerate(image):
        for x, char in enumerate(row):
            if char == '#':
                galaxies.append((x, y))

    pairs = {}
    for gal1 in galaxies:
        for gal2 in galaxies:
            pair = frozenset({gal1, gal2})
            pairs[pair] = manhattan_distance_orig(gal1, gal2)

    return sum(pairs.values())


def part2_orig(data):
    max_y = len(data)
    max_x = len(data[0])
    galaxies = []

    y = -1
    for line in data:
        y += 1
        for x, char in enumerate(line):
            if char == '#':
                galaxies.append((x, y))

    offset = 1_000_000 - 1
    y = 0
    while y < max_y:
        if all([g[1] != y for g in galaxies]):
            tmp_galaxies = []
            for g in galaxies:
                if g[1] < y:
                    tmp_galaxies.append(g)
                else:
                    g_new = g[0], g[1] + offset
                    max_y = max(max_y, g_new[1])
                    tmp_galaxies.append((g[0], g[1] + offset))
            galaxies = tmp_galaxies
            y += offset
        y += 1

    x = 0
    while x < max_x:
        if all([g[0] != x for g in galaxies]):
            tmp_galaxies = []
            for g in galaxies:
                if g[0] < x:
                    tmp_galaxies.append(g)
                else:
                    g_new = g[0] + offset, g[1]
                    max_x = max(max_x, g_new[0])
                    tmp_galaxies.append((g[0] + offset, g[1]))
            galaxies = tmp_galaxies
            x += offset
        x += 1

    pairs = {}
    for gal1 in galaxies:
        for gal2 in galaxies:
            pair = frozenset({gal1, gal2})
            pairs[pair] = manhattan_distance_orig(gal1, gal2)

    return sum(pairs.values())
