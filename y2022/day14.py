#!/usr/bin/env python

from AdventOfCode import read_data

ROCK = '█'
SAND = 'o'
AIR = ' '


class Cave:
    def __init__(self, data, part=2):
        # +x is right, +y is down
        self.deepest_rock = 0
        self.rightest_rock = 0
        self.leftest_rock = 9999
        self.world = {}
        self.sand_grains = 0
        self.part = part
        self.path = [(500, 0)]

        for line in data:
            points = line.split(' -> ')
            point = [int(x) for x in points[0].split(',')]
            for next_point in points[1:]:
                next_point = [int(x) for x in next_point.split(',')]
                sign_x = 1 if point[0] <= next_point[0] else -1
                sign_y = 1 if point[1] <= next_point[1] else -1
                for x in range(point[0], next_point[0] + sign_x, sign_x):
                    for y in range(point[1], next_point[1] + sign_y, sign_y):
                        self.world[x, y] = ROCK
                        self.deepest_rock = max(self.deepest_rock, y)
                        self.leftest_rock = min(self.leftest_rock, x)
                        self.rightest_rock = max(self.rightest_rock, x)
                point = next_point

        # For part 2, the world goes +2 downward beyond the input.
        if part == 2:
            self.deepest_rock += 2

    def print_cave(self):
        for y in range(0, self.deepest_rock+1):
            for x in range(self.leftest_rock, self.rightest_rock + 1):
                print(self.get_point((x, y)), end='')
            print()

    def get_point(self, point):
        x, y = point
        if self.part == 2 and y == self.deepest_rock:
            return ROCK
        return self.world.get((x, y), AIR)

    def sand_fall(self):
        """ Add a grain of sand to the world map and return whether there is more room for sand to pile up. """
        # Sand falls down, then down-left if block, then down-right if block, then stationary if blocked.
        x, y = self.path.pop()

        while y < self.deepest_rock:
            self.path.append((x, y))
            if self.get_point((x, y+1)) == AIR:
                y += 1
            elif self.get_point((x-1, y+1)) == AIR:
                x, y = x-1, y+1
            elif self.get_point((x+1, y+1)) == AIR:
                x, y = x+1, y+1
            else:
                # Stopped moving.
                self.path.pop()
                break

        if y >= self.deepest_rock:
            # Fell into the void.
            return False
        else:
            # Update the word map.
            self.world[x, y] = SAND
            self.sand_grains += 1
            return self.path


def day(data, part):
    cave = Cave(data, part=part)

    while cave.sand_fall():
        pass
    # cave.print_cave()

    return cave.sand_grains


def main():
    data = read_data(__file__)
    answer1 = day(data, part=1)
    answer2 = day(data, part=2)
    return answer1, answer2


expected_answers = (795, 30214)
