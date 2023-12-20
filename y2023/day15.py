#!/usr/bin/env python

from AdventOfCode import read_data


def get_hash(string):
    """ Return the 'hash' of the input string. """
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value = (current_value * 17) % 256

    return current_value


def part1(data):
    """ Return the sum of the hashes of all values (separated by commas) in the puzzle input. """
    count = 0
    for line in data:
        for split in line.split(','):
            count += get_hash(split)
    return count


def part2(data):
    """
    Add lenses into (or remove them from) boxes, where the box is chosen by the hash of the label.
    Within each box, the order of the lenses must be maintained.

    :param data: The input puzzle data as a single string in a list.
    :return: The sum of the lens' power.
    """
    # Python (3.7+) dictionaries have FIFO order, and updating a value does not change the key's order.
    boxes = [{} for _ in range(256)]
    for line in data[0].split(','):
        line = line.replace('-', '=-')
        label, lens = line.split('=')
        box = boxes[get_hash(label)]

        if lens.isdigit():
            focal = int(lens)
            box[label] = focal
        elif lens == '-':
            if label in box:
                del box[label]
        else:
            raise AssertionError

    power_sum = 0
    for box_number, box in enumerate(boxes):
        for slot, lens in enumerate(box.values(), start=1):
            power = (1 + box_number) * slot * lens
            power_sum += power

    return power_sum


def main():
    data = read_data()
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2


expected_answers = 495972, 245223
