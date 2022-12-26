#!/usr/bin/env python3

import hashlib

puzzle_input = 'iwrupvqb'


def day4(part=1):
    # Init.
    zeros = '00000'
    if part == 2:
        zeros = '000000'
    number = 1

    # Do the calculations.
    while True:
        key = f"iwrupvqb{number}"
        md5 = hashlib.md5(key.encode('utf8'))
        if md5.hexdigest().startswith(zeros):
            break
        number += 1

    # print(f"Answer for 2015 day 4 part {part}: {number}")
    return number


def main():
    answer1 = day4(part=1)
    answer2 = day4(part=2)
    return answer1, answer2


expected_answers = 346386, 9958218
