#!/usr/bin/env python
from bisect import bisect_right

from AdventOfCode import read_data


def is_fresh(ranges, ingredient):
    """
    Return True if the ingredient is within the 'fresh' ranges.

    The ranges must be sorted and non-overlapping.
    """
    index = bisect_right(ranges, ingredient, key=lambda r: r[0]) - 1
    if index == -1:
        return False
    lower, upper = ranges[index]
    if lower <= ingredient <= upper:
        return True
    return False


def both(lines):
    """
    Return the count of fresh ingredients and count of possible fresh ingredients.

    An ingredient is fresh if it falls within any of the specified ranges.
    """
    # Just read the 'fresh' ranges and sort them.
    tmp_ranges = []
    for line_index, line in enumerate(lines):
        if not line:
            break
        lower, upper = map(int, line.split('-'))
        tmp_ranges.append((lower, upper))
    tmp_ranges.sort()

    # Create a sorted list of non-overlapping ranges.
    ranges = []
    for lower, upper in tmp_ranges:
        prev_limit = ranges[-1][1] if ranges else -1
        if lower <= prev_limit <= upper:
            # Extend previous limit.
            ranges[-1] = ranges[-1][0], upper
        elif prev_limit < lower:
            # Add new limit.
            assert prev_limit < upper
            ranges.append((lower, upper))

    # Part 1: Count the available fresh ingredients.
    fresh_count = 0
    for line in lines[line_index+1:]:
        ingredient = int(line)
        if is_fresh(ranges, ingredient):
            fresh_count += 1

    # Part 2: count the types of possible fresh ingredients.
    fresh_types = 0
    for lower, upper in ranges:
        fresh_types += upper - lower + 1

    return fresh_count, fresh_types


def main():
    lines = read_data()
    return both(lines)


expected_answers = 681, 348820208020395
