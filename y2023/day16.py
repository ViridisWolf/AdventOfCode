#!/usr/bin/env python
from types import SimpleNamespace

from AdventOfCode import read_data

angle = SimpleNamespace(right=(1, 0), left=(-1, 0), up=(0, -1), down=(0, 1))


class Contraption:
    def __init__(self, data, start=((0, 0), angle.right)):
        """
        A contraption that energizes tiles as beams of light pass through them.

        :param data: The pattern of mirrors and splitters (puzzle input) as a list of strings.
        :param start: The location and direction of the starting beam.
        """
        self.width = len(data[0])
        self.height = len(data)
        self.energized = {}
        # Each beam is encoded as (location, direction).
        self.beams = [start]

        self.field = {}
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                self.field[(x, y)] = char

    @staticmethod
    def next_directions(direction, char):
        """
        Return the directions that the beam of light will exit the given tile type.

        :param direction: 2-tuple of the x and y movement vector.
        :param char: The tile type character.
        :return: The list of direction vectors that the beam will go when exiting this tile.
        """

        x, y = direction
        if char == '.':
            return [direction]
        if char == '/':
            return [(-y, -x)]
        if char == '\\':
            return [(y, x)]
        if char == '-' and x:
            return [direction]
        if char == '-' and y:
            return [angle.left, angle.right]
        if char == '|' and y:
            return [direction]
        if char == '|' and x:
            return [angle.up, angle.down]
        raise AssertionError

    def advance_beams(self):
        """ Move each beam of light forward one step, and return how many beams there are. """
        next_beams = []
        for beam in self.beams:
            location, direction = beam

            if direction in self.energized.setdefault(location, set()):
                # The beam is repeating itself, so don't bother doing anything.
                continue
            self.energized[location].add(direction)

            tile = self.field.get(location)
            for next_direction in self.next_directions(direction, tile):
                next_location = location[0] + next_direction[0], location[1] + next_direction[1]
                if 0 <= next_location[0] < self.width and 0 <= next_location[1] < self.height:
                    next_beams.append((next_location, next_direction))
        self.beams = next_beams
        return len(self.beams)

    def reset(self, start=((0, 0), angle.right)):
        """ Reset the contraption to the initial state, with the initial beam at the specified start location. """
        self.energized = {}
        self.beams = [start]


def both(data):
    """
    Simulate a beam of light being bounced around by mirrors and splitters.

    Part 1: The beam starts at the top left corner going right.
            Return how many tiles the beam passes through.
    Part 2: The beam could start at edge tile going inward.
            Return the highest tile count that any one starting beam passed through.

    :param data: The pattern of mirrors and splitters (puzzle input) as a list of strings.
    :return: 2-tuple of the answers for part 1 and part 2.
    """
    # todo: This could be made faster by changing to a recursive-like approach, where each iteration
    #       of the beams returns the places it will energize.  That could then be cached between
    #       starting locations.

    cave = Contraption(data)

    starts = [((0, y), angle.right) for y in range(cave.height)]
    starts += [((cave.width-1, y), angle.left) for y in range(cave.height)]
    starts += [((x, 0), angle.down) for x in range(cave.width)]
    starts += [((x, cave.height-1), angle.up) for x in range(cave.width)]

    energized = []
    for start in starts:
        cave.reset(start=start)
        while cave.advance_beams():
            pass
        energized.append(len(cave.energized))
    return energized[0], max(energized)


def main():
    data = read_data()
    return both(data)


expected_answers = 7788, 7987
