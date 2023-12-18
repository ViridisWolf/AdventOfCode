#!/usr/bin/env python

from AdventOfCode import read_data

def rotate_right(thingy):
    """ Return a copy the 2D array which has been rotated clockwise by 90 degrees. """
    return list(zip(*list(thingy[::-1])))


def get_symmetry_index(pattern):
    """
    Look for mirrored symmetry between top and bottom portions of the pattern.

    :param pattern: List of character sequences representing the mirror map.
    :return: Integer count of how many rows there are above the line of symmetry, or zero if symmetry was not found.
    """
    for index in range(1, len(pattern)):
        length = min(index, len(pattern) - index)
        assert length > 0
        top = pattern[:index]
        bottom = pattern[-1:index-1:-1]
        # The above is equivalent to 'bottom=list(reversed(pattern[index:]))', but is faster.

        if top[-length:] == bottom[-length:]:
            return index
    return 0


def get_index_with_smudge(pattern):
    """
    Look for mirrored symmetry between top and bottom iff there is exactly one
    character which needs to be flipped to achieve that symmetry.

    :param pattern: List of character sequences representing the mirror map.
    :return: Integer count of how many rows there are above the line of symmetry, or None if symmetry was not found.
    """
    for index in range(1, len(pattern)):
        length = min(index, len(pattern) - index)
        assert length > 0

        top = pattern[:index]
        bottom = pattern[-1:index-1:-1]
        # The above is equivalent to 'bottom=list(reversed(pattern[index:]))', but is faster.

        misses = 0
        for row1, row2 in zip(top[-length:], bottom[-length:]):
            for char1, char2 in zip(row1, row2):
                if char1 != char2:
                    misses += 1
        if misses == 1:
            return index
    return None


def part1(data):
    """
    Find the line of symmetry in each pattern of mirrors and 'summarize' them by
    adding the number of columns to the left of each symmetry line and adding
    100 times the number of rows above each symmetry line.

    :param data: The puzzle input (patterns of mirrors).
    :return: The 'summary' number.
    """
    patterns = [[]]
    for line in data:
        if not line:
            patterns.append([])
        else:
            patterns[-1].append(line)

    summary = 0
    for pattern in patterns:
        rows_above = get_symmetry_index(pattern)
        columns_left = get_symmetry_index(rotate_right(pattern))
        assert columns_left ^ rows_above
        summary += columns_left + 100*rows_above

    return summary


def part2(data):
    """
    Each mirror pattern has exactly one smudge where a character has been
    flipped, and that flipping that smudge back allows a new line of symmetry.
    Find the new line of symmetry after fixing the smudge in each pattern.

    :param data: The puzzle input (maps of mirrors).
    :return: The 'summary' number using only the new lines of symmetry.
    """
    patterns = [[]]
    for line in data:
        if not line:
            patterns.append([])
        else:
            patterns[-1].append(line)

    summary = 0
    for pattern in patterns:
        rows_above = get_index_with_smudge(pattern)
        if rows_above:
            summary += 100*rows_above
        else:
            columns_left = get_index_with_smudge(rotate_right(pattern))
            assert columns_left > 0
            summary += columns_left

    return summary


def main():
    data = read_data()
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2


expected_answers = 37113, 30449
