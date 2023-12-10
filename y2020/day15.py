#!/usr/bin/env python

from AdventOfCode import read_data


def day(data, part):
    """
    Each turn, the 'spoken' number is the age of the previous spoken number.  Find what number will be spoken at
    a certain turn.
    """
    final_turn = 2020 if part == 1 else 30000000
    numbers = {int(val): index for index, val in enumerate(data[0].split(','), 1)}
    spoken_number = numbers.popitem()[0]
    # print(f"init numbers: {numbers}, last spoken: {spoken_number}")

    for turn in range(len(numbers)+2, final_turn+1):
        spoken_turn = numbers.get(spoken_number)
        numbers[spoken_number] = turn - 1
        if spoken_turn is None:
            spoken_number = 0
        else:
            spoken_number = turn - 1 - spoken_turn
        # print(f"Turn {turn} - spoken: {spoken_number}")

    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part {part}: {spoken_number}")
    return spoken_number


def main():
    data = read_data()
    answer1 = day(data, 1)
    answer2 = day(data, 2)
    return answer1, answer2


expected_answers = 610, 1407
