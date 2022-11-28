#!/usr/bin/env python

from AdventOfCode import read_data


def manhattan_distance(p1, p2):
    """ Return the manhattan distance between two points. """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def part1():
    wire_maps = []
    for line in read_data(__file__):
        wire = set()
        wire_maps.append(wire)
        position = (0, 0)
        for move in line.split(','):
            direction = move[0]
            sign = 1 if direction in ['U', 'R'] else -1
            vertical = direction in ['U', 'D']
            amount = int(move[1:])

            for _ in range(amount):
                if vertical:
                    position = position[0] + sign, position[1]
                else:
                    position = position[0], position[1] + sign
                wire.add(position)

    overlaps = wire_maps[0].intersection(*wire_maps[1:])
    if (0, 0) in overlaps:
        overlaps.remove((0, 0))
    shortest = min(manhattan_distance((0, 0), p) for p in overlaps)

    print(f"Answer for 2019 day 3 part 1: {shortest}")


def part2():
    wire_maps = []
    for line in read_data(__file__):
        wire = {}
        wire_maps.append(wire)
        position = (0, 0)
        steps = 0

        for move in line.split(','):
            direction = move[0]
            sign = 1 if direction in ['U', 'R'] else -1
            vertical = direction in ['U', 'D']
            amount = int(move[1:])

            for _ in range(amount):
                steps += 1
                if vertical:
                    position = position[0] + sign, position[1]
                else:
                    position = position[0], position[1] + sign
                wire[position] = steps

    overlaps = [x for x in wire_maps[0].keys() if x in wire_maps[1]]
    if (0, 0) in overlaps:
        del overlaps[(0, 0)]
    shortest = min(manhattan_distance((0, 0), p) for p in overlaps)
    delay = min(wire_maps[0][k] + wire_maps[1][k] for k in overlaps)

    print(f"Answer for 2019 day 3 part 1: {shortest}")
    print(f"Answer for 2019 day 3 part 2: {delay}")


def main():
    part2()
