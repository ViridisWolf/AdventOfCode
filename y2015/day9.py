#!/usr/bin/env python
import itertools
from functools import cache

from AdventOfCode import read_data


def both_parts(locations, distances):
    """ Find the shortest path between all locations. """
    # This is a simple brute-force solution to the traveling salesman problem.  It finds both the shortest and longest
    # at the same time.

    shortest = float('inf')
    longest = float('-inf')
    for path in itertools.permutations(locations):
        loc1 = path[0]
        dist = 0
        for loc2 in path[1:]:
            dist += distances[frozenset([loc1, loc2])]
            loc1 = loc2
        shortest = min(shortest, dist)
        longest = max(longest, dist)

    return shortest, longest


def part1_branch_cut(locations, distances):
    """ Find the shortest path between all locations. """
    # This version cuts off branches as soon as that branch has exceeded the shortest known solution.

    shortest = float('inf')

    stack = [(loc1, locations-{loc1}, 0, [loc1]) for loc1 in locations]
    while stack:
        loc_current, remaining, dist, path = stack.pop()
        for loc_new in remaining:
            dist_new = dist + distances[frozenset([loc_current, loc_new])]
            if dist_new >= shortest:
                # Cut off this branch, as it's already too long.
                continue

            remaining_new = remaining - {loc_new}
            if remaining_new:
                stack.append((loc_new, remaining_new, dist_new, path+[loc_new]))
            else:
                shortest = min(shortest, dist_new)

    return shortest


def part2_branch_cut(locations, distances):
    """ Find the *longest* path between all locations. """
    @cache
    def longest_possible(points):
        """ Return the longest possible path that might exist between all the specified locations. """
        distance = 0
        for pair in itertools.combinations(points, 2):
            distance += distances[frozenset(pair)]
        return distance

    @cache
    def farthest_possible(current, others):
        """
        Return the longest possible path that might exist when starting at the specified location and then visiting
        all the other specified locations.
        """
        farthest = 0
        for loc in others:
            farthest = max(farthest, distances[frozenset([current, loc])])
        return farthest + longest_possible(others)

    longest = float('-inf')
    stack = [(loc1, locations-{loc1}, 0, [loc1]) for loc1 in locations]
    while stack:
        loc_current, remaining, dist, path = stack.pop()
        for loc_new in remaining:
            dist_new = dist + distances[frozenset([loc_current, loc_new])]
            remaining_new = remaining - {loc_new}
            if remaining_new:
                if dist_new + farthest_possible(loc_new, frozenset(remaining_new)) > longest:
                    # Keep going on this branch, as we could still get enough distance to make it the longest.
                    stack.append((loc_new, remaining_new, dist_new, path+[loc_new]))
            else:
                # All locations have been visited.
                longest = max(longest, dist_new)

    return longest


def main():
    data = read_data(__file__)

    # Parse the puzzle input data into a list of locations and the distances between them.
    distances = {}
    locations = set()
    for line in data:
        line = line.replace(' to ', ',').replace(' = ', ',')
        loc1, loc2, dist = line.split(',')
        distances[frozenset([loc1, loc2])] = int(dist)
        locations.add(loc1)
        locations.add(loc2)

    # answer1, answer2 = both_parts(locations, distances)
    answer1 = part1_branch_cut(locations, distances)
    answer2 = part2_branch_cut(locations, distances)
    return answer1, answer2


expected_answers = 117, 909
