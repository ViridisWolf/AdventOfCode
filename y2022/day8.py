#!/usr/bin/env python

import math

from AdventOfCode import read_data


def day_v1(data):
    # v1 has been replaced by v2.  They are the same algorithmically, but v2 removes code duplication.
    # Originally these two functions were at the global scope, but I nested them here to keep everything from the v1
    # solution together.
    def count_visible(trees, len_x, len_y):
        """ Return the total number of trees which are visible in the four directions from outside. """
        visible = set()

        for y in range(0, len_y):
            # Check from the left.
            last_height = -1
            for x in range(len_x):
                tree = trees[x, y]
                if tree > last_height:
                    visible.add((x, y))
                    last_height = tree

            # Check from the right.
            last_height = -1
            for x in reversed(range(len_x)):
                tree = trees[x, y]
                if tree > last_height:
                    visible.add((x, y))
                    last_height = tree

        for x in range(len_x):
            # Check from the top.
            last_height = -1
            for y in range(len_y):
                tree = trees[(x, y)]
                if tree > last_height:
                    visible.add((x, y))
                    last_height = tree

            # Check from the top.
            last_height = -1
            for y in reversed(range(len_y)):
                tree = trees[(x, y)]
                if tree > last_height:
                    visible.add((x, y))
                    last_height = tree

        return len(visible)

    def scenic_distances(trees, len_x, len_y, house):
        """ Return the number of trees that can be seen in each direction.  The side of a tree counts as being seen. """
        distances = []

        # Check to the right.
        y = house[1]
        dist = 0
        for x in range(house[0] + 1, len_x):
            tree = trees[x, y]
            dist += 1
            if tree >= trees[house]:
                break
        distances.append(dist)

        # Check to the left.
        dist = 0
        for x in range(house[0] - 1, -1, -1):
            tree = trees[x, y]
            dist += 1
            if tree >= trees[house]:
                break
        distances.append(dist)

        # Check upward.
        x = house[0]
        dist = 0
        for y in range(house[1] - 1, -1, -1):
            tree = trees[x, y]
            dist += 1
            if tree >= trees[house]:
                break
        distances.append(dist)

        # Check downward.
        x = house[0]
        dist = 0
        for y in range(house[1] + 1, len_y):
            tree = trees[x, y]
            dist += 1
            if tree >= trees[house]:
                break
        distances.append(dist)

        return distances

    # Read in the tree map (puzzle input).
    trees = {}
    len_y = len(data)
    len_x = len(data[0])
    for y, line in enumerate(data):
        for x, height in enumerate(line):
            trees[(x, y)] = int(height)

    # Part 1 calculations.
    answer = count_visible(trees, len_x, len_y)
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {answer}")

    # Part 2 calculations.
    best_score = 0
    for y in range(len_y):
        for x in range(len_x):
            distances = scenic_distances(trees, len_x, len_y, (x, y))
            score = math.prod(distances)
            best_score = max(best_score, score)
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {best_score}")


def count_visible(trees, size):
    """ Return the total number of trees which are visible in the four directions from outside. """
    visible = set()
    sx, sy = size

    # x and y encode the row or column that is being looked at.
    # dx and dy (delta x/y) encode which direction we move.
    for x, y, dx, dy in ([(   0,    y,  1,  0) for y in range(sy)] +
                         [(sx-1,    y, -1,  0) for y in range(sy)] +
                         [(   x,    0,  0,  1) for x in range(sx)] +
                         [(   x, sy-1,  0, -1) for x in range(sx)]):
        highest = -1
        while 0 <= x < sx and 0 <= y < sy:
            tree = trees[x, y]
            if tree > highest:
                visible.add((x, y))
                if tree == 9:
                    # Can't see past this tree, so might as well stop now.
                    break
                highest = tree
            x += dx
            y += dy

    return len(visible)


def scenic_distances(trees, size, house):
    """ Return the number of trees that can be seen in each direction.  The side of a tree counts as being seen. """
    distances = []
    sx, sy = size
    tree_house = trees[house]

    # Which direction we move/are looking at is encoded in dx and dy (delta x/y).
    for dx, dy in (        (0, -1),
                   (-1, 0),        (1, 0),
                           (0,  1)):
        dist = 0
        x, y = house
        x, y = x+dx, y+dy
        while 0 <= x < sx and 0 <= y < sy:
            dist += 1
            tree = trees[x, y]
            if tree >= tree_house:
                break
            # Continue along the direction we are looking.
            x += dx
            y += dy
        distances.append(dist)

    return distances


def day_v2(data):
    # Read the tree map into a dictionary.
    trees = {}
    size = len(data[0]), len(data)
    for y, line in enumerate(data):
        for x, height in enumerate(line):
            trees[(x, y)] = int(height)

    # Part 1 calculations.
    answer = count_visible(trees, size)
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {answer}")

    # Part 2 calculations.
    best_score = 0
    for y in range(size[1]):
        for x in range(size[0]):
            distances = scenic_distances(trees, size, (x, y))
            score = math.prod(distances)
            best_score = max(best_score, score)
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {best_score}")


def main():
    data = read_data(__file__)
    day_v2(data)
