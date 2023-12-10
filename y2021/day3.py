#!/usr/bin/env python

import math

from AdventOfCode import read_data


def main():
    lines = read_data()

    bits = [int(x) for x in lines[0].strip()]
    for count, line in enumerate(lines[1:]):
        line = line
        bits = [int(x) + y for x, y in zip(line, bits)]
    bits = [math.floor(x / len(lines) + 0.5) for x in bits]

    gamma = sum([1 << i for i, x in enumerate(reversed(bits)) if x])
    epsilon = (~gamma) & ((1 << len(bits)) - 1)
    power = gamma * epsilon
    # print(f"Answer for 2021 day 3 part 1: {power}")
    answer1 = power

    o2_candidates = lines[:]
    co2_candidates = lines[:]
    for index, bit in enumerate(bits):
        most_common = str(math.floor(sum([int(x[index]) for x in o2_candidates]) / len(o2_candidates) + 0.5))
        o2_candidates = [line for line in o2_candidates if line[index] == most_common]
    assert len(o2_candidates) == 1
    for index, bit in enumerate(bits):
        most_common = str(math.floor(sum([int(x[index]) for x in co2_candidates]) / len(co2_candidates) + 0.5))
        co2_candidates = [line for line in co2_candidates if line[index] != most_common]
        if len(co2_candidates) == 1:
            break
    assert len(co2_candidates) == 1

    o2_rating = int(o2_candidates[0], 2)
    co2_rating = int(co2_candidates[0], 2)
    # print(f"Answer for 2021 day 3 part 2: {o2_rating * co2_rating}")
    answer2 = o2_rating * co2_rating

    return answer1, answer2


expected_answers = 3009600, 6940518
