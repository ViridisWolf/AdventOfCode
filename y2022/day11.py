#!/usr/bin/env python

import math

from AdventOfCode import read_data


def day(data, part):
    thieves = []
    for line in data:
        line = line.strip()
        if not line:
            pass
        elif 'Monkey' in line:
            monkey = {'monkey': int(line.removeprefix('Monkey ')[:-1]),
                      'items': [],
                      'inspections': 0}
            thieves.append(monkey)
        elif 'Starting items: ' in line:
            for item in line.removeprefix('Starting items: ').split(', '):
                thieves[-1]['items'].append(int(item))
        elif 'Operation' in line:
            line = line.removeprefix('Operation: new = ')
            thieves[-1]['operation'] = eval(f"lambda old: {line}")
        elif 'Test: divisible by ' in line:
            thieves[-1]['test_div'] = int(line.removeprefix('Test: divisible by '))
        elif 'If true: throw to monkey ' in line:
            thieves[-1][True] = int(line.rsplit(' ', 1)[1])
        elif 'If false: throw to monkey ' in line:
            thieves[-1][False] = int(line.rsplit(' ', 1)[1])
        else:
            raise AssertionError

    lcm = math.lcm(*[x['test_div'] for x in thieves])

    for _ in range(20 if part == 1 else 10_000):
        for thief in thieves:
            for item in thief['items'][:]:
                if part == 1:
                    worry = thief['operation'](item) // 3
                else:
                    worry = thief['operation'](item)
                worry = worry % lcm
                test_result = worry % thief['test_div'] == 0
                accomplice = thief[test_result]
                thieves[accomplice]['items'].append(worry)

                del thief['items'][0]
                thief['inspections'] += 1

    inspections = sorted([x['inspections'] for x in thieves])
    monkey_business = inspections[-2] * inspections[-1]
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part {part}: {monkey_business}")


def main():
    data = read_data(__file__)
    day(data, part=1)
    day(data, part=2)
