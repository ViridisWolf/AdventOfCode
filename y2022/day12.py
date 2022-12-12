#!/usr/bin/env python

from AdventOfCode import read_data


def day_v1(data):
    """ Find the shortest path from the start location to the end location. """
    # This v1 solution uses an A* search algorithm adapted from a previous Advent of Code solution.

    def neighbors(point, height_map):
        """ Returns the neighbor points that are directly reachable from 'point'. """
        x, y = point
        map_width = len(height_map[0])
        map_height = len(height_map)

        current_height = height_map[y][x]

        neighs = []
        if x + 1 < map_width:
            if height_map[y][x + 1] <= (current_height + 1):
                neighs.append((x + 1, y))
        if x - 1 >= 0:
            if height_map[y][x - 1] <= (current_height + 1):
                neighs.append((x - 1, y))
        if y + 1 < map_height:
            if height_map[y + 1][x] <= (current_height + 1):
                neighs.append((x, y + 1))
        if y - 1 >= 0:
            if height_map[y - 1][x] <= (current_height + 1):
                neighs.append((x, y - 1))
        return neighs

    def get_shortest_distance(start_location, end_location, height_map):
        # Start of A* search algorithm.
        came_from = {
            start_location: None}  # Dict of which location was the previous on the best currently known path to the key node.
        visible = set([start_location])  # Which nodes are visible and need to be scanned.
        cost_from_start = {}  # Value of each item is the so-far best found cost to that node from the start.
        cost_total_est = {}  # Value of each item is the best estimated cost of a path through that node.
        cost_from_start[start_location] = 0
        cost_total_est[start_location] = 1

        while visible:
            current = min(visible, key=lambda x: cost_total_est[x])
            if current == end_location:
                # Found our way to end.
                break

            visible.remove(current)
            for neigh in neighbors(current, height_map):
                relative_g = cost_from_start[current] + 1
                if neigh not in cost_from_start or relative_g < cost_from_start[neigh]:
                    # We found a better path to this point.  Update the stats.
                    cost_from_start[neigh] = relative_g
                    cost_total_est[neigh] = relative_g + 1
                    came_from[neigh] = current
                    # Add it to the list of points to be scanned.
                    visible.add(neigh)

        best_distance = None
        if end_location in cost_from_start:
            best_distance = cost_from_start[end_location]
        return best_distance

    # Read in the map.  a-z is the height, S and E are the start and end locations.
    height_map = []
    possible_starts = []
    for y, line in enumerate(data):
        row = []
        for x, char in enumerate(line):
            if char == 'S':
                start_location = x, y
                height = 0
            elif char == 'E':
                end_location = x, y
                height = 25
            else:
                assert char in "abcdefghijklmnopqrstuvwxyz"
                height = ord(char) - ord('a')
                if char == 'a':
                    possible_starts.append((x, y))
            row.append(height)
        height_map.append(tuple(row))
    height_map = tuple(height_map)

    best = get_shortest_distance(start_location, end_location, height_map)
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {best}")

    for start_location in possible_starts:
        path_distance = get_shortest_distance(start_location, end_location, height_map)
        if path_distance is not None:
            best = min(best, path_distance)
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {best}")


def day_v2(data):
    """ Find the shortest path from the start location to the end location. """
    # This v2 version replaces the A* search with a distance map created from an exhaustive backwards walk from the end
    # location.  This is faster even for part1 of the puzzle.

    def neighbors_that_reach(point, height_map):
        """ Return list of adjacent points which can reach the specified point. """
        x, y = point
        current_height = height_map[y][x]
        neighbors = []
        for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            if 0 <= x+dx < len(height_map[0]) and 0 <= y+dy < len(height_map):
                neighbor_height = height_map[y+dy][x+dx]
                if neighbor_height + 1 >= current_height:
                    neighbors.append((x+dx, y+dy))
        return neighbors

    def mark_distances(start, height_map):
        """ Return a dict of all locations which can reach the specified point, where the value is the distance."""
        # This is a breadth-first search of all possible points that can reach 'point'.  It starts from point and walks
        # backwards to see which neighbors can reach point.
        known_distances = {start: 0}
        current_distance = 0

        visible = neighbors_that_reach(start, height_map)
        while visible:
            next_visible = []
            current_distance += 1

            # Mark all points currently visible with their distance.
            for point in visible:
                if point in known_distances:
                    continue
                # Because this is a breadth-first search, the shortest distance will be the first time we see the point.
                known_distances[point] = current_distance
                their_neighbors = neighbors_that_reach(point, height_map)
                next_visible.extend(their_neighbors)
            visible = next_visible
        return known_distances

    # Read in the map.  a-z is the height, S and E are the start and end locations.
    height_map = []
    possible_starts = []
    for y, line in enumerate(data):
        row = []
        for x, char in enumerate(line):
            if char == 'S':
                start_location = x, y
                height = 0
            elif char == 'E':
                end_location = x, y
                height = 25
            else:
                assert char in "abcdefghijklmnopqrstuvwxyz"
                height = ord(char) - ord('a')
                if char == 'a':
                    possible_starts.append((x, y))
            row.append(height)
        height_map.append(tuple(row))
    height_map = tuple(height_map)

    # Do all the mapping.
    distances = mark_distances(end_location, height_map)

    answer1 = distances[start_location]
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {distances[start_location]}")

    best = answer1
    for point in possible_starts:
        best = min(best, distances.get(point, best))
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {best}")


def main():
    data = read_data(__file__)
    day_v2(data)
