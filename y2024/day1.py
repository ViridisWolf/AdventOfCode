#!/usr/bin/env python3

from AdventOfCode import read_data


def parts(data):
    """
    The data is two groups of numbers, one group on the left and another on the right.
    Part 1: Find the sum of the differences between the two groups for the same index.
    Part 2: Sum the multiplication of the left number with the count of that number in the right group.
    """
    lefts = []
    rights = []
    for line in data:
        left, right = line.split()
        lefts.append(int(left))
        rights.append(int(right))

    lefts.sort()
    rights.sort()

    total_dists = 0
    total_mults = 0
    for index, left in enumerate(lefts):
        right = rights[index]
        total_dists += abs(left - right)

        count = rights.count(left)
        total_mults += left*count

    return total_dists, total_mults


def main():
    data = read_data()
    return parts(data)


expected_answers = 1319616, 27267728
