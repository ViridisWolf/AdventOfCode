#!/usr/bin/env python
from AdventOfCode import read_data


def find_best_battery(bank, remaining):
    """Return the best battery for the job and its location."""
    order = sorted(bank, reverse=True)

    # Discard the highest if there aren't enough characters behind it.
    while bank.index(order[0]) + remaining >= len(bank):
        order.pop(0)

    location = bank.index(order[0])
    value = bank[location]
    # print(''.join(bank), 'best choice:', value)
    return value, location


def parts(lines, length):
    """
    In a bank of batteries, find the highest 'joltage' output by wiring a specific number of batteries in sequence.

    The joltage is calculated by concatenating the individual batteries together and interpreting that as a number.
    The battery order cannot be changed.  The return value is the sum the joltages from all banks.
    """
    total_joltage = 0
    for line in lines:
        bank = [x for x in line]
        best_batteries = []
        for remaining in reversed(range(length)):
            best, location = find_best_battery(bank, remaining=remaining)
            best_batteries.append(best)
            bank = bank[location+1:]

        joltage = int(''.join(best_batteries))
        total_joltage += joltage
        # print(line, joltage)
    return total_joltage


def part1_old(lines):
    total_joltage = 0
    for line in lines:
        bank = [x for x in line]
        order = sorted(bank, reverse=True)

        # Discard the highest if it's the last character.
        if bank.index(order[0]) + 1 == len(bank):
            order.pop(0)

        first_location = bank.index(order[0])
        first = bank[first_location]
        second = sorted(bank[first_location+1:], reverse=True)[0]

        joltage = int(first + second)
        total_joltage += joltage
        # print(line, joltage)
    return total_joltage


def main():
    lines = read_data()
    return parts(lines, length=2), parts(lines, length=12)


expected_answers = 17383, 172601598658203
