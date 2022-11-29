#!/usr/bin/env python

from AdventOfCode import read_data


class TreeMap:
    def __init__(self, pattern):
        self.map = tuple(pattern)
        self.width = len(pattern[0])
        self.height = len(pattern)

    def get_square(self, x, y):
        # x = x % self.width
        # y = y % self.height
        return self.map[y][x]

    def square_is_tree(self, x, y):
        """ Returns True if the square is a tree, False if it's empty, or None if it's beyond the top/bottom. """
        if y > self.height:
            return None

        char = self.get_square(x, y)
        assert char in '.#'
        return char == '#'


def day(lines):
    # https://adventofcode.com/2020/day/3

    pattern = []
    for line in lines:
        line = tuple(line.strip())
        pattern.append(line)

    trees = TreeMap(pattern)
    tree_count = 0
    delta_x = 3
    x = 0
    for y in range(1, trees.height):
        x = (x + delta_x) % trees.width
        tree_count += trees.square_is_tree(x, y)

    print(f"Answer for 2020 day 3 part 1: {tree_count}")

    tree_mult = 1
    for delta_x, delta_y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        x = 0
        tree_count = 0
        for y in range(delta_y, trees.height, delta_y):
            x = (x + delta_x) % trees.width
            tree_count += trees.square_is_tree(x, y)
        tree_mult *= tree_count

    print(f"Answer for 2020 day 3 part 2: {tree_mult}")


def main():
    lines = read_data(__file__)
    day(lines)
