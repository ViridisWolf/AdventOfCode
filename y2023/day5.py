#!/usr/bin/env python

from AdventOfCode import read_data


def get_destination(value, table):
    """
    Find the output for the specified input value and single table/map.
    Also calculate the remaining higher seeds which will hit in the same range.

    :param value: The input source number.
    :param table: The map/table, as a dictionary of this form: {source_start: (destination_start, length)}.
    :return: 2-tuple of the destination output and the remaining seeds which will hit in the same range.
    """

    keys = sorted(table.keys())
    remaining = float('inf')
    for source_start in keys:
        destination, length = table[source_start]
        delta = value - source_start
        if 0 <= delta <= (length - 1):
            # A range has been hit.
            remaining = length - delta - 1
            return destination + delta, remaining

        if value < source_start:
            # We fell into a whole between ranges, and source_start now points at the start of the next range.
            remaining = source_start - value - 1
            break

    # We ran off the end of the map, so 'remaining' is infinite.
    assert remaining >= 0
    return value, remaining


def day5(data, part=2):
    """
    For each initial seed value, walk the value through several source-to-destination maps, and find the lowest value
    from the final map for any seed.

    Part 1: The seed list is a simple list of seed values.
    Part 2: The seed list is encoded as pairs of starting_seed and length.

    :param data: The input puzzle data containing the seeds and maps.
    :param part: Whether the seed input is interpreted using the Part 1 meaning or the Part 2 meaning.
    :return: The lowest (best) location value for any seed.
    """
    seeds = []
    maps = {}
    path = []
    best_location = float('inf')

    assert data[0].startswith('seeds')
    if part == 1:
        seeds = [(int(x), 1) for x in data[0].split()[1:]]
    elif part == 2:
        tmp = data[0].split()[1:]
        while tmp:
            seeds.append((int(tmp[0]), int(tmp[1])))
            tmp = tmp[2:]

    # Parse the maps into dictionaries.
    current_map = None
    for line in data[1:]:
        if not line.strip():
            continue
        if 'map:' in line:
            map_name = line.split()[0]
            path.append(map_name)
            current_map = {}
            maps[map_name] = current_map
            continue

        dest, source, length = [int(x) for x in line.split()]
        current_map[source] = (dest, length)

    # Walk the seeds through the maps.
    for start_seed, length in seeds:
        seed = start_seed
        while seed < start_seed + length:
            remaining_span = float('inf')
            value = int(seed)
            for segment in path:
                current_map = maps[segment]
                value, span = get_destination(value, current_map)
                remaining_span = min(remaining_span, span)
            # After traversing all the maps, remember the best (lowest) location.
            best_location = min(best_location, value)

            # remaining_span is how many more seeds we can go while still hitting in all the same map ranges.
            # If we hit in the same ranges, then any more (higher) seeds we check will only have worse (higher)
            # final outcomes.  So, skip past remaining_span seeds since they will be worse than this one.
            seed += remaining_span + 1

    return best_location


def main():
    data = read_data(__file__)
    answer1 = day5(data, part=1)
    answer2 = day5(data, part=2)
    return answer1, answer2


expected_answers = 1181555926, 37806486
