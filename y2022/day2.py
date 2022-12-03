#!/usr/bin/env python

from AdventOfCode import read_data


def day(data, part):
    # Scores: 1 for Rock, 2 for Paper, and 3 for Scissors.  0 for loss, 3 for tie, 6 for win.
    # A for Rock, B for Paper, and C for Scissors
    # For part 1:
    #   X for Rock, Y for Paper, and Z for Scissors
    # For part 2:
    #   X for loss, Y for tie, and Z for win.

    score_map = {'A': 1, 'B': 2, 'C': 3}
    score = 0

    for line in data:
        opponent, me = line.split(' ')

        # Convert from the 'XYZ' format to the 'ABC' format.
        if part == 1:
            me = {'X': 'A', 'Y': 'B', 'Z': 'C'}[me]
        elif part == 2:
            if me == 'X':
                me = {'A': 'C', 'B': 'A', 'C': 'B'}[opponent]
            elif me == 'Y':
                me = opponent
            elif me == 'Z':
                me = {'A': 'B', 'B': 'C', 'C': 'A'}[opponent]

        # Shape score.
        score += score_map[me]

        # Win/loss score.
        if me == opponent:
            score += 3
        elif (  (me == 'A' and opponent == 'C') or
                (me == 'B' and opponent == 'A') or
                (me == 'C' and opponent == 'B')):
            score += 6
        # print(f"opp: {opponent}, me: {me}, score {score}")

    print(f"Answer for 2022 day 2 part {part}: {score}")


def main():
    data = read_data(__file__)
    day(data, part=1)
    day(data, part=2)
