#!/usr/bin/env python

from AdventOfCode import read_data


def get_dest(value, table):
    for source in table:
        if value < source:
            continue

        delta = value - source
        dest, length = table[source]
        if delta <= length:
            return dest + delta

    return value


def part1(data):
    seeds = data[0].split()[1:]

    assert "seed-to-soil" in data[2]
    maps = {}
    current_map = None
    for line in data[1:]:
        if not line.strip():
            continue
        if 'map:' in line:
            map_name = line.split()[0]
            current_map = {}
            maps[map_name] = current_map
            continue

        dest, source, length = [int(x) for x in line.split()]
        current_map[source] = (dest, length)

    best_location = float('inf')

    for seed in seeds:
        current_value = int(seed)
        for segment in [
                        "seed-to-soil",
                        "soil-to-fertilizer",
                        "fertilizer-to-water",
                        "water-to-light",
                        "light-to-temperature",
                        "temperature-to-humidity",
                        "humidity-to-location",
                        ]:
            current_map = maps[segment]
            new_value = get_dest(current_value, current_map)
            current_value = new_value

        best_location = min(best_location, current_value)

    return best_location


def get_dest2(value, table):
    keys = sorted(list(table.keys()))
    remaining = float('inf')
    for source in keys:
        delta = value - source
        dest, length = table[source]
        if 0 <= delta <= (length - 1):
            remaining = length - delta - 1
            return dest + delta, remaining

        if value < source:
            # Missed the map.
            remaining = source - value - 1
            assert remaining >= 0
            break

    assert remaining >= 0
    return value, remaining


def part2(data):
    seeds = []
    tmp = data[0].split()[1:]
    while tmp:
        seeds.append((int(tmp[0]), int(tmp[1])))
        tmp = tmp[2:]

    assert "seed-to-soil" in data[2]
    maps = {}
    current_map = None
    for line in data[1:]:
        if not line.strip():
            continue
        if 'map:' in line:
            map_name = line.split()[0]
            current_map = {}
            maps[map_name] = current_map
            continue

        dest, source, length = [int(x) for x in line.split()]
        current_map[source] = (dest, length)

    best_location = float('inf')

    for start_seed, length in seeds:
        seed = start_seed
        while seed < start_seed + length:
            current_remaining = float('inf')
            current_value = int(seed)
            for segment in [
                            "seed-to-soil",
                            "soil-to-fertilizer",
                            "fertilizer-to-water",
                            "water-to-light",
                            "light-to-temperature",
                            "temperature-to-humidity",
                            "humidity-to-location",
                            ]:
                current_map = maps[segment]
                new_value, new_remaining = get_dest2(current_value, current_map)
                current_remaining = min(current_remaining, new_remaining)
                current_value = new_value

            best_location = min(best_location, current_value)
            seed += current_remaining + 1

    return best_location


def main():
    data = read_data(__file__)
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2


expected_answers = 1181555926, 37806486
