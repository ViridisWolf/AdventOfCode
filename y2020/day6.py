#!/usr/bin/env python

from AdventOfCode import read_data


int_to_letter = 'abcdefghijklmnopqrstuvwxyz'
letter_to_int = {value: index for index, value in enumerate(int_to_letter)}


def part1(lines):
    # Part one: for each group, sum the number of questions that anyone answered yes to.

    current = 0
    groups = []
    for line in lines + ['']:
        if not line:
            # Make sure that the iteration ends with an empty string so that we get into this code.
            groups.append(current)
            current = 0
            continue

        for char in line:
            current |= 1 << letter_to_int[char]

    # Convert questions to sums.
    group_sums = []
    for group in groups:
        count = bin(group).count('1')
        group_sums.append(count)

    # print(f"Answer for 2020 day 6 part 1: {sum(group_sums)}")
    return sum(group_sums)


def part2(lines):
    # Part two: for each group, sum the number of questions that everyone (not anyone) answered yes to.

    current_group = None
    groups = []
    for line in lines + ['']:
        if not line:
            # Make sure that the iteration ends with an empty string so that we get into this code.
            assert current_group is not None
            groups.append(current_group)
            current_group = None
            continue

        current_person = 0
        for char in line:
            current_person |= 1 << letter_to_int[char]
        if current_group is None:
            current_group = current_person
        current_group &= current_person

    # Convert questions to sums.
    group_sums = []
    for group in groups:
        count = bin(group).count('1')
        group_sums.append(count)

    # print(f"Answer for 2020 day 6 part 2: {sum(group_sums)}")
    return sum(group_sums)


def main():
    lines = read_data()
    answer1 = part1(list(lines))
    answer2 = part2(list(lines))
    return answer1, answer2


expected_answers = 6534, 3402
