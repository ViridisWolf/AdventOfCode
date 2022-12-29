#!/usr/bin/env python

from AdventOfCode import read_data


def get_nth_after(data, n, after):
    index = data.index(after)
    return data[(index + n) % len(data)]


def part1(data):
    # Second element of the 2-tuple indicates if this element has been processed.
    data = [(int(x), False) for x in data]

    # print(data)
    while any(p is False for (_,p) in data):
        for index, line in enumerate(data):
            datum, processed = line
            if processed:
                continue
            break

        # print(f"Processing index {index}")

        new_index = index + datum
        sign = 1 if new_index >= 0 else -1
        new_index = sign * (abs(new_index) % (len(data) - 1))
        del data[index]
        data.insert(new_index, (datum, True))

        # if index + datum < 0:
        #     new_index = (index + datum - 1) % len(data)
        # else:
        #     new_index = (index + datum) % len(data)
        # del mixed_data[index]
        # mixed_data.insert(new_index, (datum, True))

        # print(f"Moving {datum} to index {new_index}.")
        # print(data)
        # print()

    data = [x for x, y in data]

    coordinates = get_nth_after(data, 1000, 0)
    coordinates += get_nth_after(data, 2000, 0)
    coordinates += get_nth_after(data, 3000, 0)

    return coordinates


def part2(data, part):
    if part == 2:
        data = [int(x) * 811589153 for x in data]
    data = [(int(x), index) for index, x in enumerate(data)]
    orig_data = data.copy()

    for _ in range(1 if part == 1 else 10):
        for datum, orig_index in orig_data:
            index = data.index((datum, orig_index))

            new_index = index + datum
            sign = 1 if new_index >= 0 else -1
            new_index = sign * (abs(new_index) % (len(data) - 1))
            del data[index]
            data.insert(new_index, (datum, orig_index))

            # print(f"Moving {datum} to index {new_index}.")
            # print(data)
            # print()

    data = [x for x, y in data]
    coordinates = get_nth_after(data, 1000, 0)
    coordinates += get_nth_after(data, 2000, 0)
    coordinates += get_nth_after(data, 3000, 0)

    return coordinates


def main():
    data = read_data(__file__)
    answer1 = part1(data)
    answer2 = part2(data, 2)
    return answer1, answer2


expected_answers = 4267, 6871725358451
