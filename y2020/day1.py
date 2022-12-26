#!/usr/bin/env python

from AdventOfCode import read_data


def day1(lines):
    for index, num1 in enumerate(lines):
        for num2 in lines[index+1:]:
            if num1 + num2 == 2020:
                answer = num1 * num2
                break

    # print(f"Answer for 2020 day 1 part 1: {answer}")
    return answer


def day1_part2(lines):
    for index, num1 in enumerate(lines):
        for index2, num2 in enumerate(lines[index+1:]):
            if num1 + num2 > 2020:
                continue
            for num3 in lines[index2+1:]:
                if num1 + num2 + num3 == 2020:
                    answer = num1 * num2 * num3
                    break

    # print(f"Answer for 2020 day 1 part 2: {answer}")
    return answer


def main():
    lines = read_data(__file__)
    numbers = tuple(int(x) for x in lines)
    answer1 = day1(numbers)
    answer2 = day1_part2(numbers)
    return answer1, answer2


expected_answers = 1019371, 278064990
