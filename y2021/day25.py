#!/usr/bin/env python

import copy

from AdventOfCode import read_data


def part1():
    def get_wrapped_loc(loc):
        """ Return the same location, but corrected for wrapping around the edge of the field. """
        x, y = loc
        if x < 0:
            x = field_width - 1
        elif x >= field_width:
            x = 0
        if y < 0:
            y = field_height - 1
        elif y >= field_height:
            y = 0
        return x, y

    def display_field(cucumbers):
        """ Print the field. """
        for y in range(field_height):
            print(f'{y} ', end='')
            for x in range(field_width):
                char = cucumbers.get((x, y), '.')
                print(char, end='')
            print()
        print()

    cucumbers = {}
    for row, line in enumerate(read_data(__file__)):
        for x, char in enumerate(line):
            if char != '.':
                cucumbers[x,row] = char
    field_width = len(line)
    field_height = row + 1

    # These lists keeps track of which cucumbers are trying to move.
    active_east = set([loc for loc in cucumbers if cucumbers[loc] == '>'])
    active_south = set([loc for loc in cucumbers if cucumbers[loc] == 'v'])
    active_new = []
    steps = 0
    while active_new or active_east or active_south:
        # print(f"Field after {steps} steps:")
        # display_field(cucumbers)
        steps += 1
        for phase in [0, 1]:
            # phase 0 means move east, phase 1 means move south.
            for loc in active_new:
                # Figure out if there is a cucumber here, and add it to the appropriate list.
                cuc = cucumbers.get(loc, None)
                if cuc == '>':
                    active_east.add(loc)
                elif cuc == 'v':
                    active_south.add(loc)
            active_new = []

            if phase == 0:
                next_active_east = set()
                next_cucumbers = copy.deepcopy(cucumbers)
                for loc in active_east:
                    x, y = loc
                    # Most sort first so that cucumbers to the left are blocked by ones on the right.
                    new_loc = get_wrapped_loc((x+1, y))
                    if new_loc not in cucumbers:
                        # Can move.  Update 'cucumbers'.
                        next_cucumbers[new_loc] = next_cucumbers.pop(loc)
                        # Add new location to active list and also add any location which may have been waiting for the spot.
                        next_active_east.add(new_loc)
                        active_new.append(get_wrapped_loc([x-1, y]))
                        active_new.append(get_wrapped_loc([x, y-1]))
                        #print(f"{loc} moved east, and added {new_loc} to active_east and {active_new[-2:]} to active_new")
                active_east = next_active_east
                cucumbers = next_cucumbers

            if phase == 1:
                next_active_south = set()
                next_cucumbers = copy.deepcopy(cucumbers)
                for loc in sorted(active_south, key=lambda loc: loc[1]):
                    x, y = loc
                    new_loc = get_wrapped_loc((x, y+1))
                    if new_loc not in cucumbers:
                        next_cucumbers[new_loc] = next_cucumbers.pop(loc)
                        # Add new location to active list and also add any location which may have been waiting for the spot.
                        next_active_south.add(new_loc)
                        active_new.append(get_wrapped_loc((x-1, y)))
                        active_new.append(get_wrapped_loc((x, y-1)))
                        # print(f"{loc} moved south, and added {new_loc} to active_south and {active_new[-2:]} to active_new")
                active_south = next_active_south
                cucumbers = next_cucumbers

    # print(f"Steps taken to stop moving: {steps}")
    print(f"Answer for 2021 day 25 part 1: {steps}")


def main():
    part1()
