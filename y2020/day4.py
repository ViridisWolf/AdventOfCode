#!/usr/bin/env python

from AdventOfCode import read_data


def part1(lines):
    """
    Determine validity of passports, with the only requirement being that all fields (other than country) are specified.
    """

    valid_passports = []
    current = {}
    for line in list(lines) + ['']:
        # There must have a blank line at the end of the iteration for this code to work.

        if line:
            field, val = line.split(':')
            current[field] = val

        else:
            if current:
                if len(current) == 8 or (len(current) == 7 and 'cid' not in current):
                    valid_passports.append(current)
            current = {}

    # print(f"Answer for 2020 day 4 part 1: {len(valid_passports)}")
    return len(valid_passports)


def part2(lines):
    """ Determine validity of passports, including value checks for everything (except for country). """

    valid_passports = []
    current = {}
    for line in list(lines) + ['']:
        # There must have a blank line at the end of the iteration for this code to work.

        if line:
            field, val = line.split(':')
            if field == 'byr':
                if not val.isnumeric():
                    continue
                val = int(val)
                if not (1920 <= val <= 2002):
                    continue
            elif field == 'iyr':
                if not val.isnumeric():
                    continue
                val = int(val)
                if not (2010 <= val <= 2020):
                    continue
            elif field == 'eyr':
                if not val.isnumeric():
                    continue
                val = int(val)
                if not (2020 <= val <= 2030):
                    continue
            elif field == 'hgt':
                try:
                    unit = val[-2:]
                    number = int(val[:-2])
                except ValueError:
                    continue
                if unit == 'cm':
                    if not (150 <= number <= 193):
                        continue
                elif unit == 'in':
                    if not (59 <= number <= 76):
                        continue
                else:
                    continue
            elif field == 'hcl':
                if not val.startswith('#') or not val[1:].isalnum():
                    continue
            elif field == 'ecl':
                if val not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    continue
            elif field == 'pid':
                if len(val) != 9 or not val.isnumeric():
                    continue
            elif field == 'cid':
                # Ignore country ID.
                continue
            else:
                raise AssertionError

            # The field passed all checks, so allow.
            current[field] = val

        else:
            if current and len(current) == 7:
                valid_passports.append(current)
            current = {}

    # print(f"Answer for 2020 day 4 part 2: {len(valid_passports)}")
    return len(valid_passports)


def main():
    lines = read_data()
    tmp_lines = []
    for line in lines:
        if ' ' in line:
            tmp_lines.extend(line.split(' '))
        else:
            tmp_lines.append(line)
    lines = tmp_lines

    answer1 = part1(lines)
    answer2 = part2(lines)
    return answer1, answer2


expected_answers = 208, 167
