#!/usr/bin/env python

from AdventOfCode import read_data


def day(data, part):
    """ Move elements forward or backwards in the data according to their integer value. """
    if part == 2:
        data = [int(x) * 811589153 for x in data]
    data = [(int(x), index) for index, x in enumerate(data)]
    orig_data = data.copy()

    for _ in range(1 if part == 1 else 10):
        for datum, orig_index in orig_data:
            index = data.index((datum, orig_index))

            new_index = index + datum
            new_index = new_index % (len(data) - 1)
            del data[index]
            data.insert(new_index, (datum, orig_index))

    # The answer is the sum of three elements at specific locations within the data.
    data = [x for x, _ in data]
    index = data.index(0)
    coordinates = data[(index + 1000) % len(data)]
    coordinates += data[(index + 2000) % len(data)]
    coordinates += data[(index + 3000) % len(data)]

    return coordinates


def main():
    data = read_data()
    answer1 = day(data, 1)
    answer2 = day(data, 2)
    return answer1, answer2


expected_answers = 4267, 6871725358451
