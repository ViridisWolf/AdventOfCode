#!/usr/bin/env python

from AdventOfCode import read_data


LOOKBACK = 25


def day(lines):
    # Find the number which is not a sum of two numbers from the previous 25.
    for index, line in enumerate(lines):
        if index < LOOKBACK:
            continue

        valid = False
        for back in range(LOOKBACK, 0, -1):
            for front in range(1, LOOKBACK):
                if front == back:
                    break
                if lines[index-back] + lines[index-front] == line:
                    valid = True
                    # print(f"Line #{index} is valid: {line}")
                    break
            if valid:
                break
        if not valid:
            # print(f"Line #{index}, {line}, is invalid!")
            invalid_number = line
            break

    print(f"Answer for 2020 day 9 part 1: {invalid_number}")

    # Find the contiguous range which sums to the invalid number.
    low = 0
    high = 1
    while True:
        # Expand the range forward if the sum is too low, and shrink the range forward if the sum is too high.
        contiguous_range = lines[low:high+1]
        summed = sum(contiguous_range)
        if summed < invalid_number:
            high += 1
        elif summed > invalid_number:
            low += 1
        else:
            break

    # The problem asks for the largest and smallest numbers from the contiguous range.
    smallest = min(contiguous_range)
    largest = max(contiguous_range)
    print(f"Answer for 2020 day 9 part 2: {smallest + largest}")


def main():
    lines = read_data(__file__)
    lines = [int(x) for x in lines]
    day(lines)
