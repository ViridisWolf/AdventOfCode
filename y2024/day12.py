#!/usr/bin/env python3

from AdventOfCode import read_data

rotate_clockwise = {
    (0, -1): (1, 0),
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
}
directions = list(rotate_clockwise.keys())


def both_parts(data):
    """
    Find the contiguous regions of garden plots in the puzzle input, and then calculate the price of a fence around
    each region.

    Part 1: The price for a fence is the region area times the number of edges.
    Part 2: The price for a fence is the region area times the number of sides (i.e. multiple edges in a straight
            line make one side).
    """
    garden = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            garden[(x, y)] = char

    visited = set()
    regions = []
    for location, char in garden.items():
        if location in visited:
            continue

        # Flood fill.
        plots = {location}
        region = {'edges': 0, 'plots': plots, 'char': char, 'sides': 0, 'normal_map': set()}
        regions.append(region)
        stack = [location]
        while stack:
            location = stack.pop()
            visited.add(location)
            for dx, dy in directions:
                new_loc = location[0]+dx, location[1]+dy
                if garden.get(new_loc) == char:
                    if new_loc not in plots:
                        stack.append(new_loc)
                        plots.add(new_loc)
                else:
                    if new_loc not in plots:
                        region['edges'] += 1
                        region['normal_map'].add((location, (dx, dy)))

    # Side counting.
    for region in regions:
        sides = 0
        normals = region['normal_map']
        for location, direction in normals:
            # Increment the side count if this normal vector is at the end of a side.
            # Do that by looking for a matching normal vector in the direction that the side is going.
            tangent = rotate_clockwise[direction]
            if ((location[0]+tangent[0], location[1]+tangent[1]), direction) not in normals:
                sides += 1
        region['sides'] = sides

    cost_p1 = 0
    cost_p2 = 0
    for region in regions:
        cost_p1 += len(region['plots']) * region['edges']
        cost_p2 += len(region['plots']) * region['sides']
    return cost_p1, cost_p2


def main():
    data = read_data()
    return both_parts(data)


expected_answers = 1424472, 870202
