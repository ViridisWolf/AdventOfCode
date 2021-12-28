#!/usr/bin/env python

from . import read_data


def day14(loops, part):
    """ Polymerizaion """
    pair_rules = {}

    lines = read_data('day14.data')
    template = lines[0].strip()
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        if '->' in line:
            rule = line.split(' -> ')
            pair = rule[0]
            pair_rules[pair] = rule[1]
        else:
            raise AssertionError("Should not get here.")

    pattern_counts = {}
    for pat in pair_rules.keys():
        pattern_counts[pat] = template.count(pat)

    for _ in range(loops):
        next_counts = {x: 0 for x in sorted(pair_rules.keys())}
        for pair, new in pair_rules.items():
            next_counts[pair[0] + new] += pattern_counts[pair]
            next_counts[new + pair[1]] += pattern_counts[pair]
        pattern_counts = next_counts

    element_counts = {x: 0 for x in pair_rules.values()}
    for pair, count in pattern_counts.items():
        element_counts[pair[0]] += count
    element_counts[template[-1]] += 1
    # print("Element counts:", element_counts)
    counts = sorted(element_counts.values())

    print(f"Answer for day 14 part {part}: {counts[-1] - counts[0]}")

    return counts


def main():
    day14(10, 1)
    day14(40, 2)