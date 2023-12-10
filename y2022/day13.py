#!/usr/bin/env python

from functools import cmp_to_key

from AdventOfCode import read_data


def correct_order(left, right, part=2):
    """ Return True if the left is correctly 'left' of the right element, False if reversed, and None if equal. """

    if part == 1:
        true = True
        false = False
        none = None
    else:
        # When used for the sort comparator, the return values need to be numbers.
        true = -1
        false = 1
        none = 0

    if type(left) is int and type(right) is int:
        if left < right:
            return true
        elif left > right:
            return false
        return none

    if type(left) is list and type(right) is list:
        for index in range(len(left)):
            if index >= len(right):
                return false
            compare_result = correct_order(left[index], right[index], part)
            if compare_result is not none:
                return compare_result
        # No elements were different, or left list was shorter than right list.
        if len(left) < len(right):
            return true
        return none

    # Third case: mismatched types.
    assert int in [type(left), type(right)] and list in [type(left), type(right)]
    if type(left) is int:
        left = [left]
    else:
        right = [right]
    return correct_order(left, right, part)


def part1(data):
    """ Compare pairs of packets (lists), and count which pairs are in the correct order. """
    pairs = [[]]
    for line in data:
        if line:
            line = eval(line)
            pairs[-1].append(line)
        else:
            pairs.append([])

    correct_pairs = []
    for index, pair in enumerate(pairs, 1):
        left, right = pair
        result = correct_order(left, right, part=1)
        if result is True:
            correct_pairs.append(index)

    # Answer is the sum of indexes (1 based) of the pairs that are in the correct order.
    return sum(correct_pairs)


def part2(data):
    """ Sort the received packets, including two additional divider packets, and find the position of the dividers. """
    divider1, divider2 = [[2]], [[6]]
    packets = [divider1, divider2]
    for line in data:
        if line:
            line = eval(line)
            packets.append(line)

    packets.sort(key=cmp_to_key(correct_order))

    divider1_index = packets.index(divider1) + 1
    divider2_index = packets.index(divider2) + 1
    # Answer is the product of the index (1 based) of the two dividers in the sorted packets.
    return divider1_index * divider2_index


def main():
    data = read_data()
    return part1(data), part2(data)


expected_answers = (5340, 21276)
