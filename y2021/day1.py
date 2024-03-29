#!/usr/bin/env python

from AdventOfCode import read_data


def count_increases(part1=False):
    prev_value = None
    window = [None]*3
    win_index = (1, 3)
    increase = 0

    if part1:
        # Disable the sliding window for part 1.
        window = []
        win_index = (0, 0)

    lines = read_data()
    for line in lines:
        window = window[win_index[0]: win_index[1]] + [int(line.strip())]

        if None not in window:
            value = sum(window)
            if prev_value is None:
                pass
            elif value > prev_value:
                increase += 1
            prev_value = value

    # print(f"Answer for 2021 day 1 part {1 if part1 else 2}: {increase}")
    return increase


def main():
    answer1 = count_increases(part1=True)
    answer2 = count_increases()
    return answer1, answer2


expected_answers = 1616, 1645
