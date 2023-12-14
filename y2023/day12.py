#!/usr/bin/env python

from functools import cache

from AdventOfCode import read_data

@cache
def get_arrangement_count(springs, runs):
    """
    Return the number of possible valid combinations of damaged springs.

    :param springs: The row of springs as a string.
    :param runs: Tuple of how many consecutive damaged springs there are.
    :return: The count of possible arrangements.
    """
    # First check if we can't go any further.
    if not runs:
        if springs.count('#'):
            return 0
        else:
            return 1
    if len(springs) < (sum(runs) + len(runs) - 1):
        return 0

    # Continue forward looking for a run of ? or # of the correct length.
    # For each one of those, add the arrangement count of the remaining springs.
    run = runs[0]
    possible = 0

    for index in range(0, len(springs)-run+1):
        chars = springs[index:index+run]
        if chars.count('.'):
            # Can't fit the run.
            pass
        elif len(springs)-index > run and springs[index+run] == '#':
            # Can't end a run here.
            assert len(chars) == run
        else:
            possible += get_arrangement_count(springs[index+run+1:], runs[1:])

        if springs[index] == '#':
            # We can't not count a damaged spring, so this was the last option.
            break

    return possible


def day12(data, part=1):
    """
    The puzzle input is a map of damaged and undamaged springs, followed by the
    the list of the sizes of contiguous groups of damaged springs in that row.

    Part 2: Unfold the map.

    :param data: The puzzle input (map of springs) as a list of strings.
    :param part: Whether to do part 1 or part 2.
    :return: The count of how many possible arrangements there are.
    """
    arrangements = 0
    for line in data:
        # The cache from previous lines is unlikely to be helpful, so clear the
        # cache to make resizing it faster.
        get_arrangement_count.cache_clear()

        springs, runs = line.split()
        if part == 2:
            springs = '?'.join([springs]*5)
            runs = ','.join([runs]*5)

        runs = tuple([int(x) for x in runs.split(',')])
        arrangements += get_arrangement_count(springs, runs)

    return arrangements


def main():
    data = read_data()
    answer1 = day12(data, part=1)
    answer2 = day12(data, part=2)
    return answer1, answer2


expected_answers = 6958, 6555315065024
