#!/usr/bin/env python

from AdventOfCode import read_data


def part1(data):
    # The instructions are for the movement and rotation of the ship.
    direction = 90
    x, y = 0, 0

    for line in data:
        value = int(line[1:])
        match line[0]:
            case 'N':
                y += value
            case 'S':
                y -= value
            case 'E':
                x += value
            case 'W':
                x -= value
            case 'L':
                direction = (direction - value) % 360
            case 'R':
                direction = (direction + value) % 360
            case 'F':
                assert direction in [0, 90, 180, 270]
                x += value * (1 if direction == 90 else -1 if direction == 270 else 0)
                y += value * (1 if direction == 0 else -1 if direction == 180 else 0)
            case _:
                raise AssertionError
        # print(f"{line} -> {x, y}, {direction}")

    # print(f"Answer for 2020 day 12 part 1: {abs(x) + abs(y)}")
    return abs(x) + abs(y)


def part2(data):
    # The instructions refer the movement of a waypoint around the ship.

    # x and y are the ship's position, while wx and wy are the waypoint's position.
    x, y = 0, 0
    wx, wy = 10, 1

    for line in data:
        value = int(line[1:])
        match line[0]:
            case 'N':
                wy += value
            case 'S':
                wy -= value
            case 'E':
                wx += value
            case 'W':
                wx -= value
            case 'L':
                for _ in range(value // 90):
                    wx, wy = -wy, wx
            case 'R':
                for _ in range(value // 90):
                    wx, wy = wy, -wx
            case 'F':
                x += wx * value
                y += wy * value
            case _:
                raise AssertionError

    # print(f"Answer for 2020 day 12 part 2: {abs(x) + abs(y)}")
    return abs(x) + abs(y)


def main():
    data = read_data(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2


expected_answers = 1482, 48739
