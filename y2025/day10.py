#!/usr/bin/env python
import concurrent
import math
import multiprocessing

from AdventOfCode import read_data


def find_smallest_sequence_bfs(machine):
    stack = [(machine['start'], 0)]
    states = {machine['start']}
    while stack:
        value, presses = stack.pop(0)
        new_presses = presses + 1
        for button in machine['buttons']:
            new_value = value ^ button
            if new_value == 0:
                return new_presses
            if new_value not in states:
                states.add(new_value)
                stack.append((new_value, new_presses))
    raise AssertionError("Should not have reached here.")


def part1(lines):
    machines = []
    for line in lines:
        lights, remainder = line.split(' ', 1)
        requirement = lights[1:-1].replace('.', '0').replace('#', '1')
        initial = int(requirement[::-1], 2)

        button_str = remainder.replace('(', '').replace(')', '').split()[:-1]
        buttons = []
        for value in button_str:
            button = 0
            for bit in [int(x) for x in value.split(',')]:
                button |= 1 << bit
            buttons.append(button)
        machines.append({'start': initial, 'buttons': buttons})

    presses = []
    for machine in machines:
        count = find_smallest_sequence_bfs(machine)
        presses.append(count)

    return sum(presses)


def joltage_presses(machine):
    joltages = {index:jolt for index, jolt in enumerate(machine['joltage'])}
    buttons = machine['buttons']
    buttons.sort(key=lambda b: len(b), reverse=True)
    presses = joltage_recurse(joltages, buttons)
    assert presses is not None
    return machine, presses


def joltage_recurse(joltages, buttons, splits=0):
    # This function is meant to be run with the free-threaded Python build.
    joltages = {k:v for k, v in joltages.items() if v != 0}
    buttons = [b for b in buttons if all([index in joltages for index in b])]
    if not joltages:
        return 0
    elif not buttons:
        return None

    # Sort buttons so that the ones with the most variability are done last.
    button_exclusives = []
    for button in buttons:
        others = {i for b in buttons for i in b if b is not button}
        button_exclusives.append(set(button) - others)
    buttons = [b for b, _ in sorted(zip(buttons, button_exclusives), key=lambda x: len(x[1]), reverse=True)]
    assert len(buttons) == len(button_exclusives)

    button = buttons[0]
    other_buttons = buttons[1:]
    exclusive_joltage = [j for index, j in joltages.items() if not any(index in b for b in other_buttons)]

    if len(exclusive_joltage) == 0:
        # Calc the most presses possible for each button.
        highest = min([j for index, j in joltages.items() if index in button])
        other_highest = [min([j for index, j in joltages.items() if index in button]) for button in other_buttons]
        lowest = max(max(joltages.values()) - sum(other_highest), 0)
    elif len(set(exclusive_joltage)) == 1:
        highest = exclusive_joltage[0]
        if highest > min([j for index, j in joltages.items() if index in button]):
            return None
        lowest = highest
    else:
        # If there are multiple different exclusive joltages for this button, then no solution is possible.
        return None

    best = math.inf
    results = []
    if splits < 1 and (highest-lowest >= 20):
        splits += 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            jobs = {}
            for presses in range(lowest, highest+1):
                new_joltages = {index: (j - presses if index in button else j) for index, j in joltages.items()}
                jobs[executor.submit(joltage_recurse, new_joltages, other_buttons, splits)] = presses
            for job, presses in jobs.items():
                results.append((job.result(), presses))
    else:
        for presses in range(lowest, highest + 1):
            new_joltages = {index: (j - presses if index in button else j) for index, j in joltages.items()}
            results.append((joltage_recurse(new_joltages, other_buttons, splits=splits), presses))

    for subsequent_presses, presses in results:
        if subsequent_presses is None:
            continue
        else:
            if presses + subsequent_presses < best:
                best = presses + subsequent_presses
    return best if best < math.inf else None


def part2(lines):
    machines = []
    for line in lines:
        line = line.split()
        buttons = [tuple([int(x) for x in b[1:-1].split(',')]) for b in line[1:-1]]
        joltage = tuple([int(x) for x in line[-1][1:-1].split(',')])
        machines.append({'buttons':buttons, 'joltage':joltage})
        assert len(set(buttons)) == len(buttons)

    presses = []
    with multiprocessing.Pool(20) as pool:
        for result in pool.imap_unordered(joltage_presses, machines):
            presses.append(result[1])
    return sum(presses)


def main():
    lines = read_data()
    return part1(lines), part2(lines)


expected_answers = 399, 15631
