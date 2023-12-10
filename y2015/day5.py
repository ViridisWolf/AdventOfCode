#!/usr/bin/env python3

from AdventOfCode import read_data


def part1():
    nice = 0
    vowels = 'aeiou'
    bad_strings = ('ab', 'cd', 'pq', 'xy')
    lines = read_data()

    for line in lines:
        repeated = False
        vowel_count = 0
        prev = None

        if any(True for x in bad_strings if x in line):
            continue

        for index, char in enumerate(line):
            if char == prev:
                repeated = True
            prev = char
            if char in vowels:
                vowel_count += 1

        if repeated and vowel_count >= 3:
            # Don't need to check for 'bad' because we don't get here if it was bad.
            nice += 1

    # print(f"Answer for 2015 day 5 part 1: {nice}")
    return nice


def part2():
    nice = 0
    lines = read_data()

    for line in lines:
        repeated = False
        pair = False
        prev = None
        prev2 = None

        for index, char in enumerate(line):
            if char == prev2:
                repeated = True
            if prev is not None:
                if line.count(f'{prev}{char}') >= 2:
                    pair = True
            prev2 = prev
            prev = char

        if repeated and pair:
            nice += 1

    # print(f"Answer for 2015 day 5 part 2: {nice}")
    return nice


def main():
    answer1 = part1()
    answer2 = part2()
    return answer1, answer2


expected_answers = 236, 51
