#!/usr/bin/env python

from AdventOfCode import read_data


def both(lines):
    """
    Return how many times a dial hits zero after rotating left or right.

    The dial numbers go from 0 to 99, and the dial can wrap around.
    Part 1: How many times does the dial stop at zero after a rotation?
    Part 2: How many times does the dial pass or stop at zero?
    """
    limit = 100
    zeros_seen = 0
    zeros_landed = 0
    position = 50

    for line in lines:
        assert line[0] in ['R', 'L']
        direction = 1 if line[0] == 'R' else -1
        distance = int(line[1:])
        assert distance > 0

        zeros_seen += int(distance / 100)
        distance = distance % 100

        new_position = position + (direction * distance)
        if new_position >= limit:
            new_position -= limit
            zeros_seen += 1
        elif new_position < 0:
            new_position += limit
            if position != 0:
                zeros_seen += 1
        elif new_position == 0:
             zeros_seen += 1

        position = new_position
        if position == 0:
            zeros_landed += 1

    return zeros_landed, zeros_seen


def part2_old(lines):
    class State:
        limit = 100
        def __init__(self):
            self.zeros = 0
            self.position = 50
        def tick(self, direction):
            assert direction in [1, -1]
            self.position += direction
            if self.position >= self.limit:
                self.position -= self.limit
            elif self.position < 0:
                self.position += self.limit

            if self.position == 0:
                self.zeros += 1

    state = State()
    for line in lines:
        direction = 1 if line[0] == 'R' else -1
        assert line[0] in ['R', 'L']
        distance = int(line[1:])
        for _ in range(distance):
            state.tick(direction)
        print(f"{line=}, {state.position=}, {state.zeros=}")
    return state.zeros


def main():
    lines = read_data()
    return both(lines)

expected_answers = 1135, 6558
