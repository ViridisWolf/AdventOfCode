#!/usr/bin/env python

from AdventOfCode import read_data


def get_neighbors(location, heightmap, return_location=False):
    """
     Return every neighbor height for the specified location.  If return_location is True, return their locations.

    :param location: The location (x, y) to find the neighbors for.
    :param heightmap: The heightmap to use (list of lists).
    :param return_location: If True, return the point location instead of height and only return a point if its height
                            is less than 9.
    :return: Set of point locations or heights that neighbor on the specified location.
    """
    x, y = location
    xmin, xmax = location[0] - 1, location[0] + 1
    ymin, ymax = location[1] - 1, location[1] + 1
    if xmin < 0:
        xmin = 0
    elif xmax >= len(heightmap):
        xmax = len(heightmap) - 1
    if ymin < 0:
        ymin = 0
    elif ymax >= len(heightmap[0]):
        ymax = len(heightmap[0]) - 1

    neighs = set()
    for x, y in {(xmin, y), (xmax,y), (x, ymin), (x, ymax)}:
        if (x, y) == location:
            # Don't return the height of the specified point.
            continue

        height = heightmap[x][y]
        if return_location:
            # When returning the locations instead of heights, we only want points which may be in the basin.
            if height < 9:
                neighs.add((x, y))
        else:
            neighs.add(height)
    return neighs


def get_basin(location, heightmap):
    """ Return the points in the specified basin. """
    # This code assumes that each basin will always be bordered by points with height 9.
    # If there are adjacent basins with no wall of 9s between them, then this code will not work.
    basin = set()
    points = {location}
    while points:
        point = points.pop()
        basin.add(point)
        # Get neighboring locations with height < 9.
        neighs = get_neighbors(point, heightmap, return_location=True)
        for neigh in neighs:
            if neigh not in basin:
                points.add(neigh)
    return basin


def day9():
    heightmap = []
    minimums = []

    # Read in the height map.
    for y, line in enumerate(read_data()):
        for x, height in enumerate(line):
            if x >= len(heightmap):
                heightmap.append([])
            heightmap[x].append(int(height))

    # Check the height.
    for y in range(len(heightmap[0])):
        for x in range(len(heightmap)):
            height = heightmap[x][y]
            if height < min(get_neighbors((x, y), heightmap)):
                minimums.append(((x, y), height))

    risk_level = sum((m[1]+1) for m in minimums)
    # print("Answer for 2021 day 9 part 1:", risk_level)
    answer1 = risk_level

    basin_sizes = []
    for m in minimums:
        basin = get_basin(m[0], heightmap)
        basin_sizes.append(len(basin))
    # print("Basin sizes:", basin_sizes)

    mult = 1
    for size in sorted(basin_sizes)[-3:]:
        mult *= size
    # print("Answer for 2021 day 9 part 2:", mult)
    answer2 = mult

    return answer1, answer2


def main():
    return day9()


expected_answers = 532, 1110780
