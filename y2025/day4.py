#!/usr/bin/env python
from dataclasses import dataclass

from AdventOfCode import read_data

@dataclass(frozen=True)
class Point:
    """A point on 2D grid."""
    x: int
    y: int


def display(field):
    """Display the field of rolls of paper, using the same formating as shown in the puzzle."""
    min_x = min(point.x for point in field)
    max_x = max(point.x for point in field)
    min_y = min(point.y for point in field)
    max_y = max(point.y for point in field)

    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            point = Point(x, y)
            if point in field:
                if is_reachable(point, field):
                    line += 'x'
                else:
                    line += "@"
            else:
                line += "."
        print(line)


def is_reachable(roll, field):
    """Return whether the rolls of paper can be reached (has fewer than 4 neighbors)."""
    neighbors = 0
    directions = [(-1, -1), (0, -1), (1, -1),
                  (-1, 0),           (1, 0),
                  (-1, 1),  (0, 1),  (1, 1)]
    for dx, dy in directions:
        neighbor = Point(roll.x + dx, roll.y + dy)
        if neighbor in field:
            neighbors += 1
            if neighbors >= 4:
                return False
    return True


def part1(lines):
    """Return the number of rolls of paper which can be reached.

    A roll of paper can be reached if it has 3 or fewer neighboring (including diagonals) rolls of paper.
    """
    field = set()
    for y, line in enumerate(lines):
        # Get the x,y coordinates and of any "@" characters in the line.
        for x, char in enumerate(line):
            if char == "@":
                roll = Point(x, y)
                field.add(roll)

    # Count the number of points which have 3 or fewer neighbors.
    count = 0
    for roll in field:
        if is_reachable(roll, field):
            count += 1
    return count


def part2(lines):
    """Return the number of rolls of paper which can be removed.

    A roll can be removed if it is reachable, and this then may allow more rolls to be removed.
    """
    field = set()
    for y, line in enumerate(lines):
        # Get the x,y coordinates and of any "@" characters in the line.
        for x, char in enumerate(line):
            if char == "@":
                roll = Point(x, y)
                field.add(roll)

    count = 0
    while True:
        changed = False
        for roll in set(field):
            if is_reachable(roll, field):
                field.remove(roll)
                count += 1
                changed = True
        if not changed:
            break
    return count


def main():
    lines = read_data()
    return part1(lines), part2(lines)


expected_answers = 1351, 8345
