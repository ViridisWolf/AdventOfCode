#!/usr/bin/env python
import math

from AdventOfCode import read_data


def day6(data, part):
    """
    Find the number of ways that a toy boat race can be won.  The boat travels at a constant speed, and that speed is
    determined by how much time is spent not moving at the beginning of the race.  The "race" has a minimum distance
    within a fixed time limit to guarantee a win.

    :param data: The puzzle input as a list of strings.
    :param part: Whether to use the part 1 or part 2 interpretation of the puzzle input, as an integer.
    :return: The answer for one part.
    """

    if part == 1:
        time_limits = [int(x) for x in data[0].split()[1:]]
        required_distances = [int(x) for x in data[1].split()[1:]]
    else:
        time_limits = [int(''.join(data[0].split()[1:]))]
        required_distances = [int(''.join(data[1].split()[1:]))]

    win_product = 1
    for race, time_limit in enumerate(time_limits):
        distance = required_distances[race] + 1
        # Apply quadratic equation to find the two crossing points where the distance is just enough.  All of the
        # button-durations between the two crossings will be good enough to win.  The quadratic equation will give
        # real-number button-durations for the crossing points, however, and so we need to round the answers toward the
        # middle area where the distance is higher.
        first_win = math.ceil((time_limit - (time_limit**2 - 4 * distance) ** 0.5) / 2)
        last_win = math.floor((time_limit + (time_limit**2 - 4 * distance) ** 0.5) / 2)
        ways_to_win = last_win - first_win + 1
        win_product *= ways_to_win

    return win_product


def part1_old(data):
    time_limits = [int(x) for x in data[0].split()[1:]]
    required_distances = [int(x) for x in data[1].split()[1:]]

    wins_mult = 1
    for race, time_limit in enumerate(time_limits):
        ways_to_win = 0
        for duration in range(0, time_limit):
            speed = duration
            distance = speed * (time_limit - duration)
            if distance > required_distances[race]:
                ways_to_win += 1
        wins_mult *= ways_to_win

    return wins_mult


def part2_old(data):
    time_limits = [int(''.join(data[0].split()[1:]))]
    required_distances = [int(''.join(data[1].split()[1:]))]

    wins_mult = 1
    for race, time_limit in enumerate(time_limits):
        ways_to_win = 0
        for duration in range(0, time_limit):
            speed = duration
            distance = speed * (time_limit - duration)
            if distance > required_distances[race]:
                ways_to_win += 1
        wins_mult *= ways_to_win

    return wins_mult


def main():
    data = read_data()
    answer1 = day6(data, part=1)
    answer2 = day6(data, part=2)
    return answer1, answer2


expected_answers = 608902, 46173809
