#!/usr/bin/env python

import itertools
from functools import cache

from AdventOfCode import read_data

valves = {}


@cache
def get_paths(current, selectable):
    """
    Get the paths to every selectable valve location.
    
    :param current: The string name of the current valve.
    :param valves: The frozenset of the 'valves' dict.items().
    :param selectable: Which of the valves may be chosen as possible destinations.
    :return: Dictionary of the paths to every valve.  Each path includes the current valve.
    """

    global valves

    # Get the paths (and thus distances) from this valve to all other valves.
    paths = {current: [current]}
    stack = [current]
    while stack:
        valve = stack.pop()
        path = paths[valve]
        for tunnel in valves[valve]['tunnels']:
            new_path = path + [tunnel]
            if tunnel not in paths or len(paths[tunnel]) > len(new_path):
                paths[tunnel] = new_path
                # If we've found a shorter path, we'll need to re-check everything from that node.
                stack.append(tunnel)

    # Remove any destinations which are not selectable.
    paths = {k: v for k, v in paths.items() if k in selectable}

    return paths


@cache
def try_all_orders(start_location, available_time, targets):
    global valves

    if not targets:
        return 0

    done_paths = []
    # Element format: flowed, remaining time, path (where path is a list of valve names and when they were visited)
    current_paths = [[0, available_time, [(start_location, 0)]]]
    while current_paths:
        flowed, remaining_time, path_info = current_paths.pop()
        # print(path[-1])
        path = [x[0] for x in path_info]
        location = path[-1]
        # print(f"path: {path}, location: {location}")
        # Get the paths to all closed valves.
        dest_paths = get_paths(location, targets)
        # Remove already visited locations.
        dest_paths = {k: v for k, v in dest_paths.items() if k not in path}
        # Remove any valves which have no flow.
        dest_paths = {k: v for k, v in dest_paths.items() if valves[k]['flow'] > 0}

        # Go to each one, open it, and add that to the stack.
        for dest, path_to_dest in dest_paths.items():

            path_to_dest = get_paths(location, targets)[dest]
            # print(dest, path_to_dest)
            if len(path_to_dest) > remaining_time:
                # No time to reach and open the valve.
                new_time = 0
            else:
                new_flowed = flowed + valves[dest]['flow'] * (remaining_time - len(path_to_dest))
                new_time = remaining_time - len(path_to_dest)

            minute = available_time - new_time
            if len(dest_paths) == 1 or new_time <= 1:
                # This must be the last valve.
                done_paths.append((new_flowed, 0, tuple(path_info) + ((dest, minute),)))
            else:
                # Throw it back on the stack.
                assert len(dest_paths) > 1
                assert new_time > 1
                current_paths.append([new_flowed,
                                      new_time,
                                      tuple(path_info) + ((dest, minute),)])

    # We've tried all valve orders now.  Sort to find the best.
    done_paths.sort()
    best = done_paths[-1]
    flowed, remaining_time, path = best
    # print(f"Best released {flowed} pressure and went in the order of {path}")
    return flowed


def try_all_splits(start_location, available_time):
    global valves
    # Choose first which valves will be handled by the human and by the elephant.
    # For both the human and elephant, get the best possible result.
    # Try all possible combinations of splitting the valves between the human and elephant.
    human = []
    elephant = []
    valve_names = [k for k, v in valves.items() if v['flow'] > 0]
    for n in range(1, len(valve_names) + 1):
        # Don't really need to remove redundant combinations here because of caching used later.
        for combo in itertools.combinations(valve_names, n):
            human.append(combo)
            elephant.append(tuple([v for v in valve_names if v not in combo]))

    best = 0
    for pair1, pair2 in zip(human, elephant):
        result = try_all_orders(start_location, available_time, pair1)
        result += try_all_orders(start_location, available_time, pair2)
        best = max(best, result)

    return best


def day(data, part):
    global valves

    total_minutes = 30 if part == 1 else 26
    for line in data:
        valve, line = line.removeprefix('Valve ').split(' ', 1)
        flow, line = line.removeprefix('has flow rate=').split(';', 1)
        line = line.removeprefix(' tunnels lead to valves ').removeprefix(' tunnel leads to valve ')
        tunnels = line.split(', ')
        valves[valve] = {'valve': valve,
                         'flow': int(flow),
                         'tunnels': tunnels,
                         }

    if part == 1:
        flowed = try_all_orders('AA', total_minutes, tuple(valves.keys()))
    else:
        flowed = try_all_splits('AA', total_minutes)

    return flowed


def main():
    data = read_data(__file__)
    answer1 = day(data, part=1)
    answer2 = day(data, part=2)
    return answer1, answer2


expected_answers = 1751, 2207
