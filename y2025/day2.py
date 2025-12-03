#!/usr/bin/env python
from math import floor, ceil

from AdventOfCode import read_data


def part1(lines):
    """
    Find the invalid numbers in the input range of numbers, and return the sum of them.

    Invalid numbers are ones where the first half of the number is the same as the second half (in decimal).
    """
    invalid_sum = 0
    for bounds in lines[0].split(','):
        lower, upper = bounds.split('-')
        lower, upper = int(lower), int(upper)
        for product_id  in range(lower, upper + 1):
            product_str = str(product_id)
            length = len(product_str)
            if length % 2 != 0:
                continue
            if product_str[:floor(length/2)] == product_str[ceil(length/2):]:
                invalid_sum += product_id

    return invalid_sum


def part2(lines):
    """
    Find the invalid numbers in the input range of numbers, and return the sum of them.

    Invalid numbers are ones where the number (in decimal) consists of repeated patterns of any length.
    """
    invalid_sum = 0
    for bounds in lines[0].split(','):
        lower, upper = bounds.split('-')
        lower, upper = int(lower), int(upper)
        for product_id  in range(lower, upper + 1):
            product_str = str(product_id)
            max_length = len(product_str)

            for length in range(1, max_length//2 + 1):
                sequence = product_str[:length]
                if product_str == sequence*int(max_length/length):
                    invalid_sum += product_id
                    break

    return invalid_sum


def main():
    lines = read_data()
    return part1(lines), part2(lines)

expected_answers = 9188031749, 11323661261
