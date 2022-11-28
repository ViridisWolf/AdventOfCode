#!/usr/bin/env python

from AdventOfCode import read_data


def decode_seat(seat):
    assert len(seat) == 10
    assert all(x in 'FBLR' for x in seat)
    row = seat[:7].replace('F', '0').replace('B', '1')
    column = seat[-3:].replace('L', '0').replace('R', '1')

    return int(row, 2), int(column, 2)


def decode_to_id(seat):
    row, col = decode_seat(seat)
    assert row <= 127
    assert col <= 7
    return (row << 3) | col


def day(lines):
    """ Find the highest numbered seat ID. """

    seats = [None] * (128 * 8)
    lowest = 999999
    highest = -1
    for line in lines:
        seat = decode_to_id(line)
        lowest = min(lowest, seat)
        highest = max(highest, seat)
        seats[seat] = True

    # Part one: find the highest occupied seat ID.
    print(f"Answer for 2020 day 5 part 1: {highest}")

    # Part two: find the only unoccupied seat in the middle of the occupied seats.
    your_seat = seats.index(None, lowest, highest)
    print(f"Answer for 2020 day 5 part 2: {your_seat}")


def main():
    lines = read_data(__file__)
    day(lines)
