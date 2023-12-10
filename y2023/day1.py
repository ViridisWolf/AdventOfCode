#!/usr/bin/env python

import re

from AdventOfCode import read_data


def part1_orig(data):
    """
    Find the first and last number in each string, concatenate them into one whole number, and return the total for all
    strings.
    """
    total = 0

    for line in data:
        while not line[0].isdigit():
            line = line[1:]
        first_digit = line[0]
        line = line[::-1]

        while not line[0].isdigit():
            line = line[1:]
        second_digit = line[0]

        number = int(first_digit + second_digit)
        total += number
    return total


def parts(data, part=2):
    """
    Find the first and last number in each string, concatenate them into one whole number, and return the total for all
    strings.  The numbers may be spelled out with letters, and the letters may overlap.

    :param data: The puzzle data as a list of strings.
    :param part: Which part of the puzzle to do.
    :return: The answer for one part of the puzzle.
    """

    word_map = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    if part == 2:
        word_map |= {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

    pattern = "|".join(word_map.keys())
    re_pattern = re.compile(pattern)
    re_pattern_reversed = re.compile(pattern[::-1])

    total = 0
    for line in data:
        # Find the first number in the string using regex.
        match = re_pattern.search(line)
        first_digit = match.group(0)
        first_digit = word_map[first_digit]

        # To find the last number in the string, reverse both the pattern and the string.
        line = line[::-1]
        match = re_pattern_reversed.search(line)
        second_digit = match.group(0)
        # The matched value needs to be reversed before looking it up in the dictionary.
        second_digit = word_map[second_digit[::-1]]

        number = first_digit*10 + second_digit
        total += number

    return total


# def part2_orig(data):
#     # This nasty code was the result when I was trying to get to a solution as quickly as possible.
#     total = 0
#     for line in data:
#         while not any(
#                 [
#                     line.startswith('1'),
#                     line.startswith('2'),
#                     line.startswith('3'),
#                     line.startswith('4'),
#                     line.startswith('5'),
#                     line.startswith('6'),
#                     line.startswith('7'),
#                     line.startswith('8'),
#                     line.startswith('9'),
#                     line.startswith('one'),
#                     line.startswith('two'),
#                     line.startswith('three'),
#                     line.startswith('four'),
#                     line.startswith('five'),
#                     line.startswith('six'),
#                     line.startswith('seven'),
#                     line.startswith('eight'),
#                     line.startswith('nine')]):
#             line = line[1:]
#
#         if line[0].isdigit():
#             first_digit = line[0]
#         if line.startswith('one'):
#             first_digit = 1
#         if line.startswith('two'):
#             first_digit = 2
#         if line.startswith('three'):
#             first_digit = 3
#         if line.startswith('four'):
#             first_digit = 4
#         if line.startswith('five'):
#             first_digit = 5
#         if line.startswith('six'):
#             first_digit = 6
#         if line.startswith('seven'):
#             first_digit = 7
#         if line.startswith('eight'):
#             first_digit = 8
#         if line.startswith('nine'):
#             first_digit = 9
#         while not any([
#                     line.endswith('1'),
#                     line.endswith('2'),
#                     line.endswith('3'),
#                     line.endswith('4'),
#                     line.endswith('5'),
#                     line.endswith('6'),
#                     line.endswith('7'),
#                     line.endswith('8'),
#                     line.endswith('9'),
#                     line.endswith('one'),
#                     line.endswith('two'),
#                     line.endswith('three'),
#                     line.endswith('four'),
#                     line.endswith('five'),
#                     line.endswith('six'),
#                     line.endswith('seven'),
#                     line.endswith('eight'),
#                     line.endswith('nine')]):
#             line = line[:-1]
#         if line[-1].isdigit():
#             second_digit = line[-1]
#         if line.endswith('one'):
#             second_digit = 1
#         if line.endswith('two'):
#             second_digit = 2
#         if line.endswith('three'):
#             second_digit = 3
#         if line.endswith('four'):
#             second_digit = 4
#         if line.endswith('five'):
#             second_digit = 5
#         if line.endswith('six'):
#             second_digit = 6
#         if line.endswith('seven'):
#             second_digit = 7
#         if line.endswith('eight'):
#             second_digit = 8
#         if line.endswith('nine'):
#             second_digit = 9
#
#         num = int(str(first_digit) + str(second_digit))
#         total += num
#
#     return total


def main():
    data = read_data()
    answer1 = parts(data, part=1)
    answer2 = parts(data, part=2)
    return answer1, answer2


expected_answers = 55123, 55260
