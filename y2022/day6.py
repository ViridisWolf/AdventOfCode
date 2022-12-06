#!/usr/bin/env python

from AdventOfCode import read_data


def day_v1(data, part):
    """ Find the first place where the last x characters have had no repeats within that range. """

    line = data[0]
    required_len = 4 if part == 1 else 14

    for index in range(required_len, len(line)):
        if len(set(line[index-required_len:index])) == required_len:
            break
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part {part}: {index}")


def day_v4(data, part):
    """ Find the first place where the last x characters have had no repeats within that range. """

    line = data[0]
    required_len = 4 if part == 1 else 14

    for index in range(required_len, len(line)):
        segment = line[index-required_len:index]
        for char in segment:
            if segment.count(char) > 1:
                break
        else:
            # No char had multiple counts.
            break
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part {part}: {index}")


def main():
    data = read_data(__file__)
    day_v4(data, 1)
    day_v4(data, 2)
