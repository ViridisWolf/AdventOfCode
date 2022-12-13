#!/usr/bin/env python

from AdventOfCode import read_data


priority = {v: i for i, v in enumerate(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')}


def get_duplicate(line):
    """ Return the item with is in both the first of and second half of the iterable.  Must only be one such item. """
    halfway = len(line) // 2
    bag1 = line[0:halfway]
    bag2 = line[halfway:]
    for item in bag1:
        if item in bag2:
            return item


def get_common(bags):
    """ Return the item which is common between the three bags.  There must be only one such item. """
    for item in bags[0]:
        if item in bags[1] and item in bags[2]:
            return item


def part1(data):
    """ Find the sum of the 'priority' of the items which are duplicated in each bag. """
    total = 0
    for bag in data:
        item = get_duplicate(bag)
        total += priority[item]

    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {total}")
    return total


def part2(data):
    """ Find the sum of the 'priority' of each item which is common amongst each three elves' bags. """
    total = 0
    while data:
        item = get_common(data[0:3])
        data = data[3:]
        total += priority[item]

    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {total}")
    return total


def main():
    data = read_data(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2

expected_answers = 7793, 2499
