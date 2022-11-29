#!/usr/bin/env python

import re

from AdventOfCode import read_data


def static_vars(**kwargs):
    def decorator(func):
        for key in kwargs:
            setattr(func, key, kwargs[key])
        return func
    return decorator


def part1_old(lines):
    # Parse input into dict of lists.
    bag_types = {}
    for line in lines:
        bag, contents = line.split(' bags contain ')
        assert bag not in bag_types

        bag_types[bag] = []
        for subbag in contents.split(', '):
            match = re.search('\d* ?(.*?) bags?\.?', subbag)
            color = match.group(1)
            bag_types[bag].append(color)

    # Keep track of which bag types contain at least shiny bag.
    # Repeatedly loop over bag types counting and removing any which contain a shiny gold bag at some point.
    contain_shiny_gold = set()
    while bag_types:
        starting_bags = list(bag_types)
        for bag, contents in dict(bag_types).items():
            for subbag in contents:
                if subbag in contain_shiny_gold or subbag == 'shiny gold':
                    contain_shiny_gold.add(bag)
                    bag_types.pop(bag)
                    break
                if subbag == 'no other':
                    bag_types.pop(bag)
                    break
        if list(bag_types) == starting_bags:
            # No change, so remaining bags must not contain any shiny gold bags.
            break

    print(f"Answer for 2020 day 7 part 1: {len(contain_shiny_gold)}")


def day_old(lines):
    # Parse input into dict of lists, where each list contains pointers back to other entries.
    bag_types = {}
    for line in lines:
        bag_color, contents = line.split(' bags contain ')
        assert bag_color not in bag_types or not bag_types[bag_color]['contents']
        if bag_color not in bag_types:
            bag_types[bag_color] = {'color': bag_color, 'contents': []}
        bag = bag_types[bag_color]

        for item in contents.split(', '):
            match = re.search('(\d*) ?(.*?) bags?\.?', item)
            count, sub_color = match.groups()
            if sub_color == 'no other':
                continue
            if sub_color not in bag_types:
                bag_types[sub_color] = {'color': sub_color, 'contents': []}
            sub_bag = bag_types[sub_color]
            bag['contents'].append((sub_bag, int(count)))

    def count_bag_color(bag, color):
        """ Return the number of bags of the specified color that are inside the given bag. """
        total = 0
        for sub_bag, count in bag['contents']:
            if sub_bag['color'] == color:
                total += count
            else:
                total += count_bag_color(sub_bag, color) * count
        return total

    contain_shiny_gold = 0
    for bag in bag_types.values():
        if count_bag_color(bag, 'shiny gold') > 0:
            contain_shiny_gold += 1
    print(f"Answer for 2020 day 7 part 1 (alt): {contain_shiny_gold}")

    total = 0
    for color in bag_types:
        total += count_bag_color(bag_types['shiny gold'], color)
    print(f"Answer for 2020 day 7 part 2: {total}")


@static_vars(cache={})
def count_bag_color(bag, color):
    """ Return the number of bags of the specified color that are inside the given bag. """
    if (bag['color'], color) in count_bag_color.cache:
        return count_bag_color.cache[(bag['color'], color)]

    total = 0
    for sub_bag, count in bag['contents']:
        if sub_bag['color'] == color:
            # This assumes that bags will never contain any bags of their own color.  This must be true else we'd
            # have recursion and an infinite number of bags.
            total += count
        elif color is None:
            # Count all colors; i.e. count this sub_bag itself and everything inside it.
            total += count * (1 + count_bag_color(sub_bag, color))
        else:
            total += count * count_bag_color(sub_bag, color)
    count_bag_color.cache[(bag['color'], color)] = total
    return total


def day(lines):
    # Parse input into dict of lists, where each list contains pointers back to other entries.
    bag_types = {}
    for line in lines:
        bag_color, contents = line.split(' bags contain ')
        assert bag_color not in bag_types or not bag_types[bag_color]['contents']
        if bag_color not in bag_types:
            bag_types[bag_color] = {'color': bag_color, 'contents': []}
        bag = bag_types[bag_color]

        for item in contents.split(', '):
            match = re.search('(\d*) ?(.*?) bags?\.?', item)
            count, sub_color = match.groups()
            if sub_color == 'no other':
                continue
            if sub_color not in bag_types:
                bag_types[sub_color] = {'color': sub_color, 'contents': []}
            sub_bag = bag_types[sub_color]
            bag['contents'].append((sub_bag, int(count)))

    contain_shiny_gold = 0
    for bag in bag_types.values():
        if count_bag_color(bag, 'shiny gold') > 0:
            contain_shiny_gold += 1
    print(f"Answer for 2020 day 7 part 1: {contain_shiny_gold}")

    total = count_bag_color(bag_types['shiny gold'], color=None)
    print(f"Answer for 2020 day 7 part 2: {total}")


def main():
    lines = read_data(__file__)
    day(lines)
