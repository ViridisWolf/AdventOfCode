#!/usr/bin/env python

import re

from . import read_data


def day2(passwords):
    """ Calculates how many passwords are valid. """

    valids = 0
    valids_part2 = 0

    for entry in passwords:
        password = entry['password']
        char_count = password.count(entry['char'])
        if entry['min'] <= char_count <= entry['max']:
            valids += 1

        index1 = entry['min'] - 1
        index2 = entry['max'] - 1
        if bool(password[index1] == entry['char']) ^ bool(password[index2] == entry['char']):
            valids_part2 += 1

    print(f"Answer for 2020 day 2 part 1: {valids}")
    print(f"Answer for 2020 day 2 part 2: {valids_part2}")


def main():
    lines = read_data('day2.data')
    passwords = []
    for line in lines:
        match = re.search('(\d+)-(\d+) (\w): (\w+)', line)
        passwords.append({'min': int(match.group(1)),
                          'max': int(match.group(2)),
                          'char': match.group(3),
                          'password': match.group(4),
                          })
    day2(passwords)

