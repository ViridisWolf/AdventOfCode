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

    print(f"Answer for 2015 day 4 part {part}: {number}")


def main():
    day4(part=1)
    day4(part=2)
