#!/usr/bin/env python

from AdventOfCode import read_data


def day2():
    paper = 0
    ribbon = 0

    lines = read_data(__file__)
    for box in lines:
        h, w, l = [int(x) for x in box.split('x')]
        sides_area = (h*w, h*l, w*l)
        paper += 2*sum(sides_area) + min(sides_area)

        sides_len = [2*h, 2*l, 2*w]
        sides_len.sort()
        vol = h*w*l
        ribbon += vol + sum(sides_len[0:2])

    # print(f"Answer for 2015 day 2 part 1: {paper}")
    # print(f"Answer for 2015 day 2 part 2: {ribbon}")
    return paper, ribbon


def main():
    return day2()


expected_answers = 1586300, 3737498
