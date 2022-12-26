#!/usr/bin/env python

# Puzzle URL: https://adventofcode.com/2021/day/5

from AdventOfCode import read_data


DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


def day5(part=1):
    def get_line_points(line):
        """ Return the points that are crossed by the line, including the two end points."""
        p0, p1 = line
        if p1[0] < p0[0]:
            # p0 is always the left most point.
            p0, p1 = p1, p0
        if p0[0] == p1[0]:
            # Special case for a vertical line.
            y_low = min(p0[1], p1[1])
            y_high = max(p0[1], p1[1])
            line_points = set([(p0[0], y) for y in range(y_low, y_high+1)])
        else:
            # Either a horizontal line or a diagonal line.
            x = p0[0]
            y = p0[1]
            line_points = set()
            y_sign = 1 if p1[1] > y else -1 if p1[1] < y else 0
            for x in range(x, p1[0]+1):
                line_points.add((x, y))
                y += y_sign
        return line_points

    points = {}
    lines = read_data(__file__)
    for line in lines:
        line = line.split(' -> ')
        p0, p1 = line[0].split(','), line[1].split(',')
        line = (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1]))
        # print(f"Line segment: {line}")

        if part == 1 and (line[0][0] != line[1][0] and line[0][1] != line[1][1]):
            # Slanted line, skip for part one.
            continue
        new_points = get_line_points(line)
        debug(f"points covered by line {line}: {sorted(new_points)}")
        for p in new_points:
            points[p] = points.get(p, 0) + 1

    # Count the points touched by two or more lines.
    count = sum([1 for x in points.values() if x >= 2])
    # print(f"Answer for 2021 day 5 part {part}: {count}")
    assert part != 1 or count == 5835
    assert part != 2 or count == 17013
    return count


def main():
    answer1 = day5(part=1)
    answer2 = day5(part=2)
    return answer1, answer2


expected_answers = 5835, 17013
