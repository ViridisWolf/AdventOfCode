#!/usr/bin/env python
from bisect import bisect_left
from dataclasses import dataclass
from functools import cache
from itertools import zip_longest

from AdventOfCode import read_data


@dataclass(frozen=True)
class Point:
    """A point in 2D space."""
    x: int
    y: int

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return (self.x, self.y) < (other.x, other.y)
        raise NotImplemented


def part1(lines):
    # Sort by x.  Compare points from far ends of the list.

    points = []
    for line in lines:
        # x, y = [int(a) for a in line.split(',')]
        p = Point(*[int(x) for x in line.split(',')])
        points.append(p)
    points.sort(key=lambda p: p.x)
    max_y = max([p.y for p in points]) - min([p.y for p in points]) + 1

    largest_area = 0
    for index, p1 in enumerate(points[0:len(points)//2+1]):
        for p2 in points[:index:-1]:
            if largest_area > (p2.x - p1.x)*max_y:
                break
            tmp_area = (p2.x - p1.x + 1) * (abs(p2.y - p1.y) + 1)
            if tmp_area > largest_area:
                # print(f"New largest: {tmp_area} from {p1=}, {p1=}")
                largest_area = tmp_area

    return largest_area


@cache
def is_inside(point):
    """Return True if the point is within the polygon."""
    global edges_vert
    global edges_horz

    # Check if on a horizontal line.
    lower_bound = bisect_left(edges_horz, point.y, key=lambda e: e[0].y)
    for edge in edges_horz[lower_bound:]:
        if edge[0].y > point.y:
            break
        if edge[0].x <= point.x <= edge[1].x:
            return True

    # Every time an edge is crossed, we've moved from inside to outside.
    inside = False
    for edge in edges_vert:
        if edge[0].x > point.x:
            break
        assert edge[0].y <= edge[1].y
        if edge[0].y <= point.y <= edge[1].y:
            if point.x == edge[0].x:
                return True
            if edge[1].y == point.y:
                inside ^= True
            elif edge[0].y < point.y < edge[1].y:
                inside ^= True
    return inside


def edge_crossed(line):
    """Return True if the line crosses any orthogonal edge."""
    if line[0] > line[1]:
        line = tuple(reversed(line))
    if line[0].x != line[1].x:
        direction = 0
    else:
        direction = 1
    orthogonal = direction ^ 1
    edges = edges_vert if direction == 0 else edges_horz
    lower_bound = bisect_left(edges, line[0][direction], key=lambda e: e[0][direction])
    for edge in edges[lower_bound+1:]:
        if edge[0][direction] >= line[1][direction]:
            # We're past any lines which might be crossed.
            break
        if line[0][orthogonal] < edge[0][orthogonal] or line[0][orthogonal] > edge[1][orthogonal]:
            # Missed in the other axis.
            continue
        # Must have hit the edge.
        if line[0][orthogonal] == edge[0][orthogonal] or line[0][orthogonal] == edge[1][orthogonal]:
            # This crossed the end of an edge, so check the next point to see if it's in bounds.
            for delta in [-1, 1]:
                p = [edge[0][direction] + delta, line[0][orthogonal]]
                if direction == 1:
                    p.reverse()
                if not is_inside(Point(p[0], p[1])):
                    return True
        else:
            # Crossed an in the middle of an edge to the outside, assuming there aren't back-to-back edges.
            return True
    # We haven't covered the case where all the line ends on two edges, but is outside for the middle.
    # So, check that the middle of the line is inside.
    return not is_inside(Point((line[0].x+line[1].x)//2, (line[0].y+line[1].y)//2))


def part2(lines):
    """The puzzle input forms a perimeter.  Return the area of the largest rectangle that fits within it."""
    global edges_vert
    global edges_horz
    polygon = []
    points = []
    for line in lines:
        p = Point(*[int(x) for x in line.split(',')])
        points.append(p)

    for p1, p2 in zip_longest(points, points[1:], fillvalue=points[0]):
        edge = (p1, p2) if p1 < p2 else (p2, p1)
        polygon.append(edge)

    points.sort(key=lambda p: p.x)
    edges_vert = sorted([edge for edge in polygon if edge[0].x == edge[1].x], key=lambda e: e[0].x)
    edges_horz = sorted([edge for edge in polygon if edge[0].y == edge[1].y], key=lambda e: e[0].y)

    max_height = max([p.y for p in points]) - min([p.y for p in points]) + 1
    largest_area = 0
    for index, p1 in enumerate(points[:len(points)//2+1]):
        for p2 in points[:index:-1]:
            if largest_area >= (p2.x - p1.x)*max_height:
                break
            p3 = Point(p1.x, p2.y)
            p4 = Point(p2.x, p1.y)
            rect_lines = (p1, p3), (p3, p2), (p2, p4), (p4, p1)
            if any(edge_crossed(line) for line in rect_lines):
                continue

            area = (p2.x - p1.x + 1) * (abs(p2.y - p1.y) + 1)
            if area > largest_area:
                largest_area = area

    return largest_area


def main():
    lines = read_data()
    return part1(lines), part2(lines)


expected_answers = 4767418746, 1461987144
