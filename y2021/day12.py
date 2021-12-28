#!/usr/bin/env python

from pprint import pprint

from . import read_data


class Cave:
    big = 'big'
    small = 'small'

    def __init__(self, name):
        self.name = name
        self.type = self.big if name.isupper() else self.small
        self.connections = set()

    def add_connection(self, connection):
        """ Add a new connecting Cave objects. """
        self.connections.add(connection)

    def get_connections(self):
        """ Return the set of connecting Cave objects. """
        return self.connections


def get_paths(start, caves, end='end', revisit_small_cave=False):
    """ Return all possible paths to the end. """
    start = caves[start]
    paths_ended = []
    paths_ongoing = [[start]]

    while paths_ongoing:
        # Select which path to continue along.
        path = paths_ongoing.pop()
        cave = path[-1]

        if cave.name == end:
            # We're done!
            paths_ended.append(path)
            continue

        # Find all the connections from this cave.
        connections = cave.get_connections()
        for connection in connections:
            if connection == start:
                continue
            elif connection.name == end:
                pass
            # Check if another small cave is there.
            elif connection.type is Cave.small and connection in path:
                if not revisit_small_cave:
                    continue
                # Check to see if a small cave has already been visited twice.
                smalls = [c.name for c in path if c.type is Cave.small]
                if len(smalls) != len(set(smalls)):
                    # Already have a duplicate small cave; can't add another.
                    continue

            # Make a new longer path for each connection.
            new_path = list(path)
            new_path.append(connection)
            paths_ongoing.append(new_path)

    return paths_ended


def day12(part):
    caves = {}

    for line in read_data('day12.data'):
        name1, name2 = line.split('-')
        if name1 not in caves:
            caves[name1] = Cave(name1)
        if name2 not in caves:
            caves[name2] = Cave(name2)
        cave1 = caves[name1]
        cave2 = caves[name2]
        cave1.add_connection(cave2)
        cave2.add_connection(cave1)

    paths = get_paths('start', caves, end='end', revisit_small_cave=True if part == 2 else False)
    # paths = [[c.name for c in path] for path in paths]
    # pprint(sorted(paths))
    print(f"Answer for day 12 part {part} is: {len(paths)}")


def main():
    day12(part=1)
    day12(part=2)
