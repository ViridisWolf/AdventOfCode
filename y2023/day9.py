#!/usr/bin/env python

from AdventOfCode import read_data


def derivative(numbers):
    """ Return the numerical derivative of the input list of numbers. """
    output = []
    for index, num in enumerate(numbers):
        if index >= len(numbers) - 1:
            break
        output.append(numbers[index+1] - num)
    return output


def get_constant(history, part):
    if all([x == 0 for x in history]):
        return 0

    diff = derivative(history)
    if part == 1:
        constant = history[-1]
        constant += get_constant(diff, part)
    else:
        constant = history[0]
        constant -= get_constant(diff, part)
    return constant


def both(data):
    post_constants = []
    pre_constants = []
    for line in data:
        history = [int(x) for x in line.split()]
        pre_constants.append(get_constant(history, 1))
        post_constants.append(get_constant(history, 2))

    return sum(pre_constants), sum(post_constants)


def main():
    data = read_data(__file__)
    return both(data)


expected_answers = 1819125966, 1140
