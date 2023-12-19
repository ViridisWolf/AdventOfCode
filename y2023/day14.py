#!/usr/bin/env python

from AdventOfCode import read_data


class Platform:
    def __init__(self, data):
        """
        Create new 'platform' instance from the provided map.

        :param data: The initial state of the platform (puzzle input) as a list of strings.
        """
        self.max_y = len(data) - 1
        self.max_x = len(data[0]) - 1
        self.cubes = set()
        self.rocks = set()

        for y, line in enumerate(data):
            for x, char in enumerate(line):
                if char == 'O':
                    self.rocks.add((x, y))
                elif char == '#':
                    self.cubes.add((x, y))

    def tilt(self, direction):
        """
        Tilt the platform in the specified direction, letting the rocks roll
        until they are blocked by something.

        :param direction: 2-tuple representing the direction to tilt: (x, y).  Westward is -x, northward is -y.
        :return: None.
        """
        dx, dy = direction
        tmp_rocks = set()
        key_func = lambda x: -x[0]*dx - x[1]*dy
        # key_func must sort the rocks to that rocks at the bottom of the tilt are first.
        for x, y in sorted(self.rocks, key=key_func):
            steps = 1
            while True:
                next_location = x + dx*steps, y + dy*steps
                if (    next_location not in self.cubes
                        and next_location not in tmp_rocks
                        and 0 <= next_location[0] <= self.max_x
                        and 0 <= next_location[1] <= self.max_y):
                    steps += 1
                else:
                    steps -= 1
                    next_location = x + dx*steps, y + dy*steps
                    break
            tmp_rocks.add(next_location)
        self.rocks = tmp_rocks

    def get_load(self):
        """ Return the current 'load' on the north support columns. """
        load = 0
        for rock in self.rocks:
            x, y = rock
            load += self.max_y + 1 - y
        return load

    def display(self):
        """ Print the current platform map. """
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                char = '.'
                if (x, y) in self.cubes:
                    char = '#'
                elif (x, y) in self.rocks:
                    char = 'O'
                print(char, end='')
            print()


def part1(data):
    """
    The puzzle input is a map of round and cubic rocks on a platform.  The round
    rocks will roll when the platform is tilted in one of the four cardinal
    directions.

    Calculate the 'load' on the support columns at the north of the platform.

    :param data: The puzzle input (map of the platform's initial state), as a list of strings.
    :return: The load on the north support columns after tilting the platform northward.
    """
    plat = Platform(data)
    plat.tilt((0, -1))
    return plat.get_load()


def part2(data):
    """
    Same as part 1, except do 1 billion "spin cycles" instead of just tilting once.

    :param data: The puzzle input (map of the platform's initial state), as a list of strings.
    :return: The load on the north support columns after doing all of the spin cycles.
    """
    plat = Platform(data)
    history = {}
    cycles = 1_000_000_000
    cyclic = False

    for cycle in range(1, cycles + 1):
        for direction in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            plat.tilt(direction)
        rocks = frozenset(plat.rocks)

        if not cyclic:
            if rocks in history:
                cyclic = True
                start = history[rocks]
                period = cycle - history[rocks]
                remaining = (cycles - start) % period
            history[rocks] = cycle
        else:
            assert history[rocks] - start == (cycle - start) % period
            if (cycle - start) % period == remaining:
                return plat.get_load()


def main():
    data = read_data()
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2


expected_answers = 110128, 103861
