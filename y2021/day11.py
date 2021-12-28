#!/usr/bin/env python

from . import read_data

DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


def get_neighbors(location, field):
    """ Return the neighboring points for the specified location. """
    r, c = location
    rmin, rmax = r - 1, r + 1
    cmin, cmax = c - 1, c + 1
    if rmin < 0:
        rmin = 0
    elif rmax >= len(field):
        rmax = len(field) - 1
    if cmin < 0:
        cmin = 0
    elif cmax >= len(field[0]):
        cmax = len(field[0]) - 1

    neighs = set()
    for r in range(rmin, rmax + 1):
        for c in range(cmin, cmax + 1):
            if (r, c) == location:
                # Don't return the specified point.
                continue
            neighs.add((r, c))
    return neighs


def update_dumbo(location, field, reset=False):
    """ Do a step of this dumbo and do any consequent actions. """
    global flashes
    r, c = location
    field[r][c] += 1
    if field[r][c] == 10:
        flashes += 1
        neighs = get_neighbors(location, field)
        # debug(f"Neighbors of {location}: {neighs}")
        for neigh in get_neighbors(location, field):
            update_dumbo(neigh, field)


def display_field(field):
    """ Print the field. """
    for row in field:
        print(row)


def day11(part):
    global flashes
    flashes = 0
    field = []
    steps = 100
    if part == 2:
        # Set steps to arbitrarily high.
        steps = 9999999

    for y, line in enumerate(read_data('day11.data')):
        row = []
        for char in line:
            row.append(int(char))
        field.append(row)

    if DEBUG:
        display_field(field)

    for step in range(steps):
        old_flashes = flashes
        for r, row in enumerate(field):
            for c, col in enumerate(row):
                update_dumbo((r, c), field)

        # Reset to zero if needed.
        for row in field:
            for c in range(len(row)):
                if row[c] >= 10:
                    row[c] = 0

        # Check for part 2 end condition.
        if part == 2 and (flashes - old_flashes) == sum([1 for r in field for c in r]):
            # All flashed on same step.
            print(f"Answer for day 11 part 2: {step+1}")
            return

        # Display the field like the example does.
        if DEBUG:
            print(f"\nAfter {step+1} steps:")
            display_field(field)

    print(f"Answer for day 11 part 1: {flashes}")


def main():
    day11(part=1)
    day11(part=2)
