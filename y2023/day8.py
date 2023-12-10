#!/usr/bin/env python
import math

from AdventOfCode import read_data


def get_step_count(node, pattern, nodes):
    """
    Return the number of steps it takes to reach an ending node (a node where the name ends with 'Z').

    :param node: The node to start at.
    :param pattern: The left/right pattern to take, as a list of integers.
    :param nodes: The dictionary of tuples of where each node leads to.
    :return: The number of steps it took to reach an end node.
    """
    steps = 0
    while True:
        for direction in pattern:
            steps += 1
            node = nodes[node][direction]
            if node[-1] == 'Z':
                return steps


def both(data):
    """
    Find the number of steps it takes to reach an ending node.

    Part 1: There is only ony starting node: 'AAA'.
    Part 2: Every node ending with 'A' is a starting node, and every path must reach an ending node at the same time,
            else they continue.

    :param data: The puzzle input as a list of strings.
    """
    nodes = {}
    starting = []
    pattern = [0 if x == 'L' else 1 for x in data[0]]
    for line in data[2:]:
        node = line.split(None, 1)[0]
        left, right = line[7:-1].split(', ')
        nodes[node] = (left, right)
        if node[-1] == 'A':
            starting.append(node)

    # Calculate the path length for each starting node on its own.  Each path should reach a periodically repeating
    # pattern.  Then, the point where all repeating patters line up together will be the least-common-multiple of their
    # path lengths.

    # This assumes:
    # 1) That each path immediately enters its repeating pattern instead of only entering the pattern some time later.
    # 2) That each path only ever includes one ending node.
    # Neither of those two assumptions are guaranteed by the wording of the puzzle, but they are true for the actual
    # puzzle input.

    counts = {}
    for start in starting:
        counts[start] = get_step_count(start, pattern, nodes)
    return counts['AAA'], math.lcm(*counts.values())


def main():
    data = read_data()
    return both(data)


expected_answers = 19637, 8811050362409
