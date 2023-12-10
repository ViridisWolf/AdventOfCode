#!/usr/bin/env python

from AdventOfCode import read_data


def part1(adapters):
    # Puzzle: When arranged in a working order, how many adaptors have a delta of 1 or 3 from the previous adaptor?
    deltas = {1: 0, 2: 0, 3: 0}
    prev = 0
    for adapter in adapters:
        # The adapter list has already been sorted and sorted order should always be a working arrangement if any work.
        assert 1 <= adapter - prev <= 3
        deltas[adapter - prev] += 1
        prev = adapter

    # print(f"Answer for 2020 day 10 part 1: {deltas[1] * deltas[3]}")
    return deltas[1] * deltas[3]


def part2(adapters):
    # Puzzle: How many ways the adapters can be arranged to reach the required jolts?

    # Each adapter can work with an input joltage of 1-3 jolts lower than itself, so there are at most 3 possible
    # adapters that can fit.  The total ways to get to a specific joltage is the sum of the ways to get to those 3
    # previous joltages.

    ways_to = {0: 1}
    for jolt in adapters:
        ways_to[jolt] = 0
        for prev_jolt in range(jolt-3, jolt):
            ways_to[jolt] += ways_to.get(prev_jolt, 0)

    # print(f"Answer for 2020 day 10 part 2: {ways_to.popitem()[1]}")
    return ways_to.popitem()[1]


def main():
    # The numbers in the data file represent "jolt" ratings for adapters.
    lines = read_data()
    lines = sorted([int(x) for x in lines])
    # Add the "built-in" adaptor, which is 3 higher than the largest adaptor in the input.
    lines.append(lines[-1] + 3)

    answer1 = part1(lines)
    answer2 = part2(lines)
    return answer1, answer2


expected_answers = 2368, 1727094849536
