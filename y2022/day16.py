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
    """
    Try all possible orders to open the valves, and return the highest amount of pressure that can be released.

    :param start_location: The starting location.
    :param available_time: The amount of time remaining.
    :param targets: The available target valves, which must have positive flow rate.
    :return: The highest amount of pressure that can be released.
    """

    # This breadth-first stack based approach is 7x faster for part 1 compared to the recursive function, but is
    # 2.3x slower on part 2.

    global valves

    if not targets:
        return 0

    # done_paths = []
    best_flow = 0

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

        # Go to each one, open it, and add that to the stack.
        for dest, path_to_dest in dest_paths.items():
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
                # done_paths.append((new_flowed, 0, tuple(path_info) + ((dest, minute),)))
                best_flow = max(best_flow, new_flowed)
            else:
                # Throw it back on the stack.
                assert len(dest_paths) > 1
                assert new_time > 1
                current_paths.append([new_flowed,
                                      new_time,
                                      tuple(path_info) + ((dest, minute),)])

    return best_flow


@cache
def get_best_flow_recursive(start_location, available_time, targets):
    """
    Try all possible orders to open the valves, and return the highest amount of pressure that can be released.

    :param start_location: The starting/current location.
    :param available_time: The amount of time remaining.
    :param targets: The available target valves, which must have positive flow rate.
    :return: The highest amount of pressure that can be released.
    """

    # This depth-first recursive version is about 7x slower for part 1 than the breadth-first stack, but 2.3x
    # faster for part 2.

    global valves

    if not targets or available_time <= 1:
        return 0

    best_flow = 0

    for destination, path in get_paths(start_location, targets).items():
        new_time = available_time - len(path)
        if new_time <= 1 or len(targets) == 1:
            continue

        new_flowed = valves[destination]['flow'] * new_time
        new_flowed += get_best_flow_recursive(destination, new_time, tuple(t for t in targets if t != destination))
        best_flow = max(best_flow, new_flowed)

    return best_flow


def try_all_splits(start_location, available_time):
    global valves
    # Choose first which valves will be handled by the human and by the elephant.
    # For both the human and elephant, get the best possible result.
    # Try all possible combinations of splitting the valves between the human and elephant.
    human = []
    elephant = []
    valve_names = [k for k, v in valves.items() if v['flow'] > 0]
    for n in range(len(valve_names)//4, len(valve_names)//2 + 1):
        # Don't really need to remove redundant combinations here because of caching used later.
        for combo in itertools.combinations(valve_names, n):
            human.append(combo)
            elephant.append(tuple([v for v in valve_names if v not in combo]))

    best = 0
    for pair1, pair2 in zip(human, elephant):
        result = get_best_flow_recursive(start_location, available_time, pair1)
        result += get_best_flow_recursive(start_location, available_time, pair2)
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
        flowed = get_best_flow_recursive('AA', total_minutes, tuple(k for k, v in valves.items() if v['flow'] > 0))
    else:
        flowed = try_all_splits('AA', total_minutes)

    return flowed


def main():
    data = read_data(__file__)
    answer1 = day(data, part=1)
    answer2 = day(data, part=2)
    return answer1, answer2


expected_answers = 1751, 2207
