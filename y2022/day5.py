#!/usr/bin/env python

from AdventOfCode import read_data

import re


def day_v1(data, part):
    # Replaced by newer versions.  This version uses string replacement during stack initialization, and moves crates
    # one at a time for part 1.
    data = data.copy()
    stacks = {}

    while True:
        line = data.pop(0)
        if '[' not in line:
            assert not data.pop(0)
            break
        line = line.replace('    ', '.').replace('[', '').replace(']', '').replace(' ', '')
        for stack, crate in enumerate(line, 1):
            if crate == '.':
                continue
            if stack not in stacks:
                stacks[stack] = []
            stacks[stack].append(crate)

    for line in data:
        match = re.search(r"move (\d+) from (\d+) to (\d+)", line)
        assert match
        count, stack_from, stack_to = [int(x) for x in match.groups()]

        if part == 1:
            for _ in range(count):
                crate = stacks[stack_from].pop(0)
                stacks[stack_to].insert(0, crate)
        else:
            crates = stacks[stack_from][0:count]
            stacks[stack_from] = stacks[stack_from][count:]
            stacks[stack_to] = crates + stacks[stack_to]

    answer = ''
    for index, stack in sorted(stacks.items()):
        answer += stack[0]
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part {part}: {answer}")


def day_v2(data, part):
    # This is modified from v1 in two ways:
    # 1) This version transposes the initial stack text so that each stack will be a single line.
    # 2) The movement code has be simplified to only use the part2 method from v1.
    stacks = {}

    blank = data.index('')
    stack_text = [''.join(index) for index in zip(*data[:blank])]
    for line in stack_text:
        line = line.strip()
        if not line.isalnum():
            continue
        # Each line should now end with the stack number, and the rest should be the stack contents.
        stacks[int(line[-1])] = list(line[:-1].strip())

    for line in data[blank+1:]:
        match = re.search(r"move (\d+) from (\d+) to (\d+)", line)
        count, source, dest = [int(x) for x in match.groups()]

        crates = stacks[source][0:count]
        if part == 1:
            crates.reverse()
        stacks[source] = stacks[source][count:]
        stacks[dest] = crates + stacks[dest]

    answer = ''.join([s[0] for s in stacks.values()])
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part {part}: {answer}")


def day_v3(data, part):
    """ Read in an initial stack structure, perform the specified movements, and print the final top crates. """
    # v3 differs from v2 in a few ways:
    # 1) Stack initialization is changed to use slicing instead of transposition.
    # 2) The order within each stack is inverted, as benchmarks showed this to be slightly faster.
    # 3) For speed, regex parsing of the move instruction is replaced with split().
    # 4) When removing crates from a stack, `del` is used instead of creating a new list.  Small speed improvement.

    # Initialize the stacks.
    stacks = {}
    for index, line in enumerate(data):
        if '[' not in line:
            break
        for stack, crate in enumerate(line[1::4], 1):
            if stack not in stacks:
                stacks[stack] = []
            if crate != ' ':
                stacks[stack].insert(0, crate)

    # Perform the move operations.
    for line in data[index+2:]:
        _, count, _, source, _, dest = line.split(' ')
        count, source, dest = int(count), int(source), int(dest)

        crates = stacks[source][-count:]
        if part == 1:
            crates.reverse()
        del stacks[source][-count:]
        stacks[dest].extend(crates)

    answer = ''.join([s[-1] for s in stacks.values()])
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part {part}: {answer}")


def main():
    data = read_data(__file__)
    day_v3(data, 1)
    day_v3(data, 2)
