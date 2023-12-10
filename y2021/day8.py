#!/usr/bin/env python

# Puzzle URL: https://adventofcode.com/2021/day/8


from AdventOfCode import read_data


def day8():
    """ Figure out which signals are which for a seven-segment display. """

    output_counts = {x: 0 for x in range(10)}
    sum_total = 0

    # Parse the input into a more usable format.
    displays = []
    lines = read_data()
    for line in lines:
        patterns = []
        outputs = []
        line = line.split(' | ')
        digits = line[0].split()
        for digit in digits:
            # Convert string digit into set of signals.
            digit = set(d for d in digit)
            patterns.append(digit)
        for digit in line[1].split():
            # Convert string digit into set of signals.
            digit = set(d for d in digit)
            outputs.append(digit)
        displays.append((patterns, outputs))


    for patterns, outputs in displays:
        # Figure out which segments are which.
        count_2 = [p for p in patterns if len(p) == 2][0]
        count_3 = [p for p in patterns if len(p) == 3][0]
        count_4 = [p for p in patterns if len(p) == 4][0]
        count_5s = [p for p in patterns if len(p) == 5]
        count_6s = [p for p in patterns if len(p) == 6]
        count_7 = [p for p in patterns if len(p) == 7][0]

        right = count_2
        top = count_3.difference(right)
        UL_middle = count_4.difference(right)
        # Every 5-count has middle, but some don't have upper_left.  Intersection means middle without upper left.
        upper_left = UL_middle.difference(set.intersection(*count_5s))
        middle = UL_middle.difference(upper_left)
        # '3' with everything except bottom removed.
        bottom = [p for p in count_5s if right.issubset(p)][0].difference(top, right, middle)
        left = count_7.difference(top, right, middle, bottom)
        lower_left = left.difference(upper_left)

        # Convert the output into numbers.
        display_number = []
        for output in outputs:
            if len(output) == 6 and not (output & middle):
                digit = 0
            elif len(output) == 2:
                digit = 1
            elif len(output) == 5 and (output >= lower_left):
                digit = 2
            elif len(output) == 5 and not (output & left):
                digit = 3
            elif len(output) == 4:
                digit = 4
            elif len(output) == 5 and (output > upper_left):
                digit = 5
            elif len(output) == 6 and not (output > right):
                digit = 6
            elif len(output) == 3:
                digit = 7
            elif len(output) == 7:
                digit = 8
            elif len(output) == 6 and (output > (upper_left | right)):
                digit = 9
            else:
                raise AssertionError

            output_counts[digit] += 1
            display_number.append(str(digit))

        sum_total += int(''.join(display_number))

    part1_count = sum([v for k, v in output_counts.items() if k in [1, 4, 7, 8]])

    # print(f"Answer for 2021 day 8 part 1: {part1_count}")
    # print(f"Answer for 2021 day 8 part 2: {sum_total}")
    return part1_count, sum_total


def main():
    return day8()


expected_answers = 365, 975706
