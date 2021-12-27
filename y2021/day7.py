#!/usr/bin/env python

# Puzzle URL: https://adventofcode.com/2021/day/6

import statistics

from . import read_data


def day7(part=2):
    # Part one seems like it should just be the average of the crab positions.
    lines = read_data('day7.data')
    positions = [int(x) for x in lines[0].split(',')]

    if part == 1:
        average = statistics.median(positions)
        best = sum(abs(p - average) for p in positions)
    elif part == 2:
        best = None
        for center in range(min(positions), max(positions)+1):
            total = 0
            for p in positions:
                delta = abs(p - center)
                total += delta*(delta + 1)/2
            if best is None or total < best:
                best = total
    else:
        raise AssertionError("'part' must be 1 or 2.")

    print(f"Answer for day 7 part {part}: {int(best)}")

def main():
    day7(part=1)
    day7(part=2)
