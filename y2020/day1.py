#!/usr/bin/env python

from AdventOfCode import read_data


def day1(numbers):
    """Find the first two numbers which sum to 2020, then multiply them together."""
    large = []
    small = []
    for num in numbers:
        # Assumption: Each number is unique.  If there were duplicates, 1010 would need to be added to `large` too.
        if num < 1010:
            small.append(num)
        else:
            large.append(num)

    for num1 in large:
        for num2 in small:
            if num1 + num2 == 2020:
                return num1 * num2
    raise AssertionError


def day1_part2(numbers):
    """Find the first three numbers which sum to 2020, then multiply them together."""
    for index, num1 in enumerate(numbers):
        for index2, num2 in enumerate(numbers[index + 1:]):
            if num1 + num2 > 2020:
                continue
            for num3 in numbers[index2 + 1:]:
                if num1 + num2 + num3 == 2020:
                    answer = num1 * num2 * num3
                    break

    # print(f"Answer for 2020 day 1 part 2: {answer}")
    return answer


def main():
    lines = read_data()
    numbers = tuple(int(x) for x in lines)
    answer1 = day1(numbers)
    answer2 = day1_part2(numbers)
    return answer1, answer2


expected_answers = 1019371, 278064990
