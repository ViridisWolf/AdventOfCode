#!/usr/bin/env python

from AdventOfCode import read_data


def both(lines):
    """
    Part1: Find invalid values on tickets and return their sum.
    Part2: Determine which field is which, and return the product of all the "departure" fields on your ticket.
    """
    field_ranges = {}
    for index, line in enumerate(lines):
        if not line:
            break
        field, ranges = line.split(': ')
        ranges = [tuple(map(int, part.split('-'))) for part in ranges.split(' or ')]
        field_ranges[field] = ranges
    all_ranges = [x for ranges in field_ranges.values() for x in ranges]
    all_ranges.sort(key=lambda x: x[0])

    assert lines[index + 1] == 'your ticket:'
    your_ticket = [int(x) for x in lines[index+2].split(',')]

    assert lines[index + 4] == 'nearby tickets:'
    other_tickets = []
    for index, line in enumerate(lines[index + 5:], start=index + 5):
        ticket = [int(x) for x in line.split(',')]
        other_tickets.append(ticket)

    # Look for any impossible value on each ticket.
    valid_tickets = []
    error_rate = 0
    for ticket in other_tickets:
        ticket_valid = True
        for field_value in ticket:
            valid = False
            for lower, upper in all_ranges:
                if lower <= field_value <= upper:
                    valid = True
                    break
                if field_value < lower:
                    break
            if not valid:
                ticket_valid = False
                error_rate += field_value
        if ticket_valid:
            valid_tickets.append(ticket)

    # On the remaining tickets, calculate which field names a field index could be.  Remove a field name from the
    # possibilities if it would make any ticket invalid.
    name_possibilities = [list(field_ranges.keys()) for _ in field_ranges]
    for index, possibilities in enumerate(name_possibilities):
        for name in possibilities[:]:
            valid = True
            rng1, rng2 = field_ranges[name]
            lower1, upper1 = rng1
            lower2, upper2 = rng2
            for ticket in valid_tickets:
                if (not (lower1 <= ticket[index] <= upper1)) and (not (lower2 <= ticket[index] <= upper2)):
                    valid = False
                    break
            if not valid:
                possibilities.remove(name)
        if len(possibilities) == 1:
            # If we've gotten this field index down to one possibility, then don't bother trying it for other indexes.
            name = possibilities[0]
            for fields_possible in name_possibilities:
                if name in fields_possible and len(fields_possible) > 1:
                    fields_possible.remove(name)

    # Determine which field name belongs to each field index iteratively removing the known field names from the
    # possibilities of other fields.
    unknowns = name_possibilities[:]
    while unknowns:
        for names in unknowns[:]:
            if len(names) == 1:
                unknowns.remove(names)
                name = names[0]
                for other in unknowns:
                    if name in other:
                        other.remove(name)

    # Calculate the part2 answer of the product of the "departure" fields in your ticket.
    departures = 1
    for index, name in enumerate(name_possibilities):
        name = name[0]
        if name.startswith('departure'):
            departures *= your_ticket[index]
    return error_rate, departures


def main():
    data = read_data()
    return both(data)


expected_answers = 32842, 2628667251989
