#!/usr/bin/env python

from functools import cache

from AdventOfCode import read_data


class Valley:
    # +x is right, +y is down.
    def __init__(self, data):
        self.walls = set()
        self.initial_blizzards = {}

        self.height = len(data) - 2
        self.width = len(data[0]) - 2
        # self.period = math.lcm(self.height, self.width)
        self.start = (0, -1)
        self.end = (self.width - 1, self.height)

        # Create a full-size set of empty sets, then remove elements from it if we find a blizzard there.
        self.blank_valley = set((x, y) for x in range(self.width) for y in range(self.height))
        # Add the starting and ending spaces.
        self.blank_valley.add(self.start)
        self.blank_valley.add(self.end)

        # Now remove any spots which have a blizzard in them.
        for y, line in enumerate(data, -1):
            for x, char in enumerate(line, -1):
                if char == '#':
                    self.walls.add((x, y))
                elif char == '.':
                    pass
                else:
                    assert char in "<>v^"
                    self.initial_blizzards[(x, y)] = char

    def get_blizzards(self, minute):
        """ Return the set of blizzard locations at the specified minute. """
        new_blizzards = {}
        for blizzard, char in self.initial_blizzards.items():
            x, y = blizzard
            if char == '>':
                dx, dy = 1, 0
            elif char == '<':
                dx, dy = -1, 0
            elif char == '^':
                dx, dy = 0, -1
            elif char == 'v':
                dx, dy = 0, 1
            else:
                raise AssertionError
            dx *= minute
            dy *= minute
            new_location = (x + dx) % self.width, (y + dy) % self.height

            if new_location not in new_blizzards:
                new_blizzards[new_location] = char
            else:
                if type(new_blizzards[new_location]) is str:
                    new_blizzards[new_location] = 2
                else:
                    new_blizzards[new_location] += 1
        return new_blizzards

    @cache
    def get_clear(self, minute):
        """
        Return a set containing the clear spots in the valley.

        The same Set object will be returned for a given minute until .cache_clear() is called on this function.  This
        means that external changes to this object will persist through to the next caller.
        """
        spots = self.blank_valley.copy()
        for location in self.get_blizzards(minute).keys():
            spots.remove(location)
        return spots

    def get_possible_moves(self, location, minute):
        """ Return all possible places that could be moved to next turn. """
        x, y = location
        possible_locations = []
        clears = self.get_clear(minute)
        for dx, dy in [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)]:
            next_loc = (x + dx), (y + dy)
            if next_loc in clears:
                possible_locations.append(next_loc)
        return possible_locations

    def get_shortest_path(self, start, end, start_minute=0):
        """ Return one of the shortest possible paths from the source to the destination. """
        # self.get_clear.cache_clear()
        done = None
        stack = [[start]]
        while stack and not done:
            next_stack = []
            minute = start_minute + len(stack[0])
            clear_spots = self.get_clear(minute)
            for path in stack:
                location = path[-1]
                if location == end:
                    done = path
                    break
                for new_location in self.get_possible_moves(location, minute):
                    if new_location in clear_spots:
                        clear_spots.remove(new_location)
                        next_stack.append(path + [new_location])
            stack = next_stack

        return done

    def print(self, minute, overlay=None):
        """
        Print out the blizzard map at the specified minute.

        :param minute: How many turns have passed.
        :param overlay: A dict which can be used to replace the character shown for specified points.
        :return: None.
        """
        if overlay is None:
            overlay = {}
        blizzards = self.get_blizzards(minute)
        for y in range(-1, self.height + 1):
            line = ""
            for x in range(-1, self.width + 1):
                char = overlay.get((x, y))
                if char is None and (x, y) in self.walls:
                    char = '#'
                elif char is None:
                    char = str(blizzards.get((x, y), '.'))
                line += char
            print(line)


def day(data):
    death = Valley(data)
    path = death.get_shortest_path(death.start, death.end, start_minute=0)
    minutes = len(path) - 1
    answer1 = minutes

    path = death.get_shortest_path(death.end, death.start, start_minute=minutes)
    minutes += len(path) - 1
    path = death.get_shortest_path(death.start, death.end, start_minute=minutes)
    minutes += len(path) - 1
    answer2 = minutes

    return answer1, answer2


def main():
    data = read_data(__file__)
    return day(data)


expected_answers = 279, 762
