#!/usr/bin/env python

from . import read_data


def day1(lines):
    for index, num1 in enumerate(lines):
        for num2 in lines[index+1:]:
            if num1 + num2 == 2020:
                answer = num1 * num2
                break

    print(f"Answer for 2020 day 1 part 1: {answer}")


def day1_part2(lines):
    for index, num1 in enumerate(lines):
        for index2, num2 in enumerate(lines[index+1:]):
            if num1 + num2 > 2020:
                continue
            for num3 in lines[index2+1:]:
                if num1 + num2 + num3 == 2020:
                    answer = num1 * num2 * num3
                    break

    print(f"Answer for 2020 day 1 part 1: {answer}")


def main():
    lines = read_data('day1.data')
    numbers = tuple(int(x) for x in lines)
    day1(numbers)
    day1_part2(numbers)
