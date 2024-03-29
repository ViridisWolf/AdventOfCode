#!/usr/bin/env python

# Puzzle URL: https://adventofcode.com/2021/day/6

from AdventOfCode import read_data


def day6(part=2):
    def get_new_fishies(cycle, count):
        """ Return a list of the count of fish in cycle type. """
        cycle -= 1
        if cycle < 0:
            return [(6, count), (8, count)]
        return [(cycle, count)]

    if part == 1:
        days = 80
    else:
        days = 256

    fish_counts_by_cycle = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    lines = read_data()
    for line in lines:
        for char in line.split(','):
            fish_counts_by_cycle[int(char)] += 1

    for day in range(days):
        new_fish_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        for cycle, count in fish_counts_by_cycle.items():
            for new_cycle, new_count in get_new_fishies(cycle, count):
                new_fish_counts[new_cycle] += new_count
        fish_counts_by_cycle = new_fish_counts

    total = sum(fish_counts_by_cycle.values())
    # print(f"Answer for 2021 day 6 part {part}: {total}")
    return total


def main():
    answer1 = day6(part=1)
    answer2 = day6(part=2)
    return answer1, answer2


expected_answers = 355386, 1613415325809
