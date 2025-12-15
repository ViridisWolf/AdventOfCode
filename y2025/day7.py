#!/usr/bin/env python
from dataclasses import dataclass
from functools import cache

from AdventOfCode import read_data


@dataclass(frozen=True)
class Point:
    """A point on 2D grid."""
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return self.__class__(self.x + other[0], self.y + other[1])
        else:
            raise NotImplemented

    def __radd__(self, other):
        return self.__add__(other)


@cache
def get_splits(beam):
    """Return the number of times that the beam gets split."""
    global limit, splitters, hit_splitters
    if beam.y >= limit:
        return
    if beam + (0, 1) in splitters:
        hit_splitters.add(beam + (0, 1))
        get_splits(beam + (-1, 1))
        get_splits(beam + (1, 1))
    else:
        get_splits(beam + (0, 1))
    return len(hit_splitters)


@cache
def new_timelines(beam):
    """Return the number of new timelines created by the beam."""
    global splitters, limit
    if beam.y >= limit:
        timelines = 0
    elif beam + (0, 1) in splitters:
        timelines = 1
        timelines += new_timelines(beam + (-1, 1))
        timelines += new_timelines(beam + (+1, 1))
    else:
        timelines = new_timelines(beam + (0, 1))
    return timelines


def both(lines):
    """
    A beam of tachyons is being fired down into a manifold of beam splitters.

    Part 1: Return how many times the beam is split.
    Part 2: There is only one tachyon.  Instead of splitters creating two new beams, they create separate timelines
            where the tachyon went one direction in each timeline.  Return the number of timelines.
    """
    global limit, splitters, hit_splitters
    limit = len(lines)
    splitters = set()
    hit_splitters = set()

    beam = Point(lines[0].index('S'), 1)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '^':
                splitters.add(Point(x, y))

    splits = get_splits(beam)
    timelines = 1 + new_timelines(beam)
    return splits, timelines


def main():
    lines = read_data()
    return both(lines)


expected_answers = 1570, 15118009521693
