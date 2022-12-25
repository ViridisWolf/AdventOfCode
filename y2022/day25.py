#!/usr/bin/env python

from AdventOfCode import read_data


def from_snafu(number):
    """ Convert a 'SNAFU' number string to an integer. """
    # SNAFU number are base 5 and only use digits 2, 1, 0, - (-1), and = (-2).
    total = 0
    number = reversed(number)
    for index, char in enumerate(number):
        if char == '-':
            value = -1
        elif char == '=':
            value = -2
        else:
            value = int(char)
        total += value * (5**index)
    return total


def to_snafu(number):
    """ Return a 'SNAFU' formatted number string for the specified integer. """

    # Divide out 5, add the remainder as the required value in that spot.
    # Then, iterate over values finding any that are 3 or 4.  If found, add one
    # to the next section and replace with '=' (for 3) or '-' (for 3).

    snafu = []
    while number:
        remainder = number % 5
        number = number // 5
        snafu.append(remainder)

    while any(True for x in snafu if x > 2):
        index = 0
        while index < len(snafu):
            number = snafu[index]
            if number >= 3:
                snafu[index] -= 5
                if index+1 == len(snafu):
                    snafu.append(0)
                snafu[index + 1] += 1
            index += 1

    # Finally, convert the integers to strings.
    for index, number in enumerate(snafu):
        if number == -2:
            snafu[index] = '='
        elif number == -1:
            snafu[index] = '-'
        else:
            assert number in [0, 1, 2]
            snafu[index] = str(number)

    return ''.join(reversed(snafu))


def day(data):
    total = 0
    for line in data:
        total += from_snafu(line.strip())
    return to_snafu(total)


def main():
    data = read_data(__file__)
    answer1 = day(data)
    return answer1,


expected_answers = "2=0-2-1-0=20-01-2-20",
