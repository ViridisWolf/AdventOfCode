#!/usr/bin/env python

from AdventOfCode import read_data


def get_connecting(pos, pipes):
    """
    Return the locations of pipes which connect to the specified pipe.

    :param pos: The location of the pipe to find the connections for.
    :param pipes: The dictionary of all pipes.
    :return: List of the connecting pipe locations.
    """
    x, y = pos
    char = pipes[(x, y)]
    connecting = []
    if char in ['|', 'L', 'J', 'S']:
        if pipes.get((x, y-1)) in ['|', 'F', '7', 'S']:
            connecting.append((x, y-1))
    if char in ['7', '|', 'F', 'S']:
        if pipes.get((x, y+1)) in ['|', 'L', 'J', 'S']:
            connecting.append((x, y+1))
    if char in ['-', 'J', '7', 'S']:
        if pipes.get(((x-1), y)) in ['-', 'L', 'F', 'S']:
            connecting.append((x-1, y))
    if char in ['-', 'F', 'L', 'S']:
        if pipes.get(((x+1), y)) in ['-', 'J', '7', 'S']:
            connecting.append(((x+1), y))

    return connecting


def get_next_connection(pos, pipes, previous):
    """
    Return the location of the next pipe in the circular path.

    :param pos: Location of the current pipe.
    :param pipes: Dictionary of all pipes in the path.
    :param previous: Location of the previous pipe in the path.
    :return: The location in of the next pipe in the path.
    """
    connections = get_connecting(pos, pipes)
    assert len(connections) == 2
    connections.remove(previous)
    return connections[0]


def start_pipe_type(start, pipes):
    """ Return the type of pipe that is at the start position. """
    # This assumes that the start position has exactly two connecting pipes.
    x, y = start
    possible = {'|', '-', '7', 'F', 'L', 'J'}
    if pipes.get((x, y-1)) in ['|', '7', 'F']:
        possible.intersection_update({'|', 'L', 'J'})
    if pipes.get((x-1, y)) in ['-', 'F', 'L']:
        possible.intersection_update({'-', 'J', '7'})
    if pipes.get((x+1, y)) in ['-', '7', 'J']:
        possible.intersection_update({'-', 'F', 'L'})
    if pipes.get((x, y+1)) in ['|', 'L', 'J']:
        possible.intersection_update({'|', '7', 'F'})
    assert len(possible) == 1
    return possible.pop()


def both(data):
    """
    Find the circular path of pipes which 'S' is part of.

    Part 1: Return the number of steps to the farthest pipe in the loop.
    Part 2: Return the count of tiles enclosed by the path.

    :param data: The puzzle input (pipe map) as a list of strings.
    :return: 2-tuple of the distance and area answers.
    """

    width = len(data[0])
    height = len(data)
    # Parse the input into a dictionary.
    start = None
    pipes = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '.':
                continue
            if char == 'S':
                start = x, y
            pipes[(x, y)] = char

    # Find the circular path.  Arbitrarily choose one of the connecting pipes to start with.
    path = {start: start_pipe_type(start, pipes)}
    location = get_connecting(start, pipes)[0]
    previous = start
    while location != start:
        path[location] = pipes[location]
        location, previous = get_next_connection(location, pipes, previous), location
    distance = len(path)//2

    # Now to find the contained area.  Start by scanning each row from the left.  We start the row outside the pipes,
    # and we are then inside the pipes if we have crossed an odd number of pipes to get there.
    # Tangentially touching a bend in the pipes does not count as crossing, but orthogonally touching a bend does count.
    crossed = area = 0
    bend = False
    for y in range(height):
        for x in range(width):
            char = path.get((x, y))
            if char == '|':
                crossed += 1
            elif char in ['L', 'F']:
                # Entering a bend.
                assert bend is False
                bend = char
            elif char == '-':
                # Continuing a bend.
                assert bend is not False
            elif char in ['J', '7']:
                # Leaving a bend.
                assert bend is not False
                bend = bend + char
                if bend in ['L7', 'FJ']:
                    crossed += 1
                else:
                    # We only touched this bend tangentially, so it doesn't change anything.
                    assert bend in ['LJ', 'F7']
                bend = False
            else:
                # Not on the pipe path.
                assert bend is False
                if crossed % 2:
                    area += 1

    return distance, area


def main():
    data = read_data()
    return both(data)


expected_answers = 6942, 297
