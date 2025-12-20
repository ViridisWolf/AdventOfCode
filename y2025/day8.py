#!/usr/bin/env python
from dataclasses import dataclass

from AdventOfCode import read_data


@dataclass(frozen=True)
class Point:
    """A point in 3D space."""
    x: int
    y: int
    z: int


def dist_sq(p1, p2):
    """Return the distance squared between two points."""
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2


def both(lines):
    """
    Find the shortest distances between junction boxes (the puzzle input), and connect them into circuits.

    Part 1: Do the 1000 shortest pairings.
    Part 2: Do as many pairings as needed until all boxes are part of one circuit.
    """
    p1_limit = 10 if len(lines) < 100 else 1000  # Allow using the example input.
    circuits = dict()   # The circuits, indexed by each junction box.
    matched = set()     # Keeps track of which junction boxes are part of any circuit.

    boxes = []
    for line in lines:
        x, y, z = [int(x) for x in line.split(',')]
        boxes.append(Point(x, y, z))

    # Create a list for each box, where each list contains tuples of the other boxes and their distances.
    # The first item in each list is the item the list is sorted relative to.
    array = []
    for box in boxes:
        tmp = [(b, dist_sq(box, b)) for b in boxes]
        array.append(sorted(tmp, key=lambda b: b[1]))

    # The top of each list will be the min distance for that box, so the shortest of all will be the min of the row.
    found_count = 0
    while array:
        found_count += 1
        # Find the minimum distance.
        array.sort(key=lambda l: l[1][1])
        (box0, _), (box1, _) = array[0][0:2]
        # The next shortest should be the same pair in the other direction.  Delete both.
        assert array[1][1][0] == array[0][0][0]
        del array[0][1], array[1][1]
        if len(array[1]) < 2:
            del array[1]
        if len(array[0]) < 2:
            del array[0]

        # Add it to the circuits.
        if box0 in matched and box1 in matched:
            # Merge circuits.
            if circuits[box0] is not circuits[box1]:
                circuits[box0].update(circuits[box1])
                for p in circuits[box1]:
                    circuits[p] = circuits[box0]
        elif box0 in matched:
            circuits[box0].add(box1)
            circuits[box1] = circuits[box0]
        elif box1 in matched:
            circuits[box1].add(box0)
            circuits[box0] = circuits[box1]
        else:
            circuits[box0] = {box0, box1}
            circuits[box1] = circuits[box0]
        matched.add(box0)
        matched.add(box1)

        if found_count == p1_limit:
            # Part 1 answer: the multiplication of the sizes of the three largest circuits after connecting 1000 pairs.
            dist_mult = 1
            for circuit in sorted(set(frozenset(s) for s in circuits.values()), key=len, reverse=True)[0:3]:
                dist_mult *= len(circuit)
        if len(matched) == len(boxes):
            # Part 2 answer: the multiplication of the x part of the last pair to be connected (stopping when all boxes
            #                are in one circuit).
            x_mult = box0.x * box1.x
            break

    return dist_mult, x_mult


def main():
    lines = read_data()
    return both(lines)


expected_answers = 175500, 6934702555
