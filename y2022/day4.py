#!/usr/bin/env python

from AdventOfCode import read_data


def day_old(data):
    # This is a rushed implementation.
    fully_contained = 0
    overlap = 0
    for line in data:
        elf1, elf2 = line.split(',')
        elf1_range = elf1.split('-')
        elf1_range = list(range(int(elf1_range[0]), int(elf1_range[1])+1))
        elf2_range = elf2.split('-')
        elf2_range = list(range(int(elf2_range[0]), int(elf2_range[1]) + 1))
        if all([i in elf2_range for i in elf1_range]) or all([i in elf1_range for i in elf2_range]):
            fully_contained += 1
        if any([i in elf2_range for i in elf1_range]) or any([i in elf1_range for i in elf2_range]):
            overlap += 1

    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {fully_contained}")
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {overlap}")


def day(data):
    """
    Calculate how many elf pairs are fully and partially overlapping.

    :param data: The puzzle input data, as a list of strings.
    :return: None
    """
    full_overlap = 0
    partial_overlap = 0
    for line in data:
        elf1, elf2 = line.split(',')
        elf1 = [int(x) for x in elf1.split('-')]
        elf2 = [int(x) for x in elf2.split('-')]
        if elf1[0] > elf2[0] or (elf1[0] == elf2[0] and elf1[1] < elf2[1]):
            # elf1 must be the lower-starting elf.  If starting at the same spot, elf1 must be the larger.
            elf1, elf2 = elf2, elf1

        if elf1[1] >= elf2[1]:
            # Given they way elf1 and elf2 were sorted above, elf1 ending after elf2 means a full overlap.
            full_overlap += 1
        elif elf2[0] <= elf1[1]:
            # Elf2 starting below/equal the max of the lower elf means a partial overlap.
            partial_overlap += 1

    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {full_overlap}")
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {full_overlap + partial_overlap}")


def main():
    data = read_data(__file__)
    day(data)
