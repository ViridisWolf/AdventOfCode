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


# Not used.
def get_constant_recursive(history, part):
    """
    Return the prefix or postfix extrapolation constant for the input history.

    :param history: The history as a list of numbers.
    :param part: Whether to do the prefix (part=2) or postfix (part=1) calculation.
    :return: The calculated extrapolation constant.
    """

    if all([x == 0 for x in history]):
        return 0

    diff = derivative(history)
    if part == 1:
        constant = history[-1] + get_constant_recursive(diff, part)
    else:
        constant = history[0] - get_constant_recursive(diff, part)
    return constant


def calc_constants(diffs):
    """
    Return the forward and backwards extrapolation constants from the derivative input.

    :param diffs: List of diff lists, including the original history value.
    :return: 2-tuple of the backwards and forwards extrapolation constants.
    """
    pre_constant = 0
    post_constant = 0
    for diff in reversed(diffs):
        pre_constant = diff[-1] + pre_constant
        post_constant = diff[0] - post_constant
    return pre_constant, post_constant


def both(data):
    """
    For all given sets of sensor history values, calculate a forward and backwards extrapolation value.
    Then sum the forwards and sum the backwards extrapolation values for all sensor histories.

    :param data: The input sensor history values, as a list of strings.
    :return: 2-tuple of the sum of forward extrapolations and sum of backwards extrapolations.
    """
    post_constants = []
    pre_constants = []
    for line in data:
        history = [int(x) for x in line.split()]
        diffs = [history]
        while not all([x == 0 for x in history]):
            history = derivative(history)
            diffs.append(history)

        pre,  post = calc_constants(diffs)
        pre_constants.append(pre)
        post_constants.append(post)

    return sum(pre_constants), sum(post_constants)


def main():
    data = read_data()
    return both(data)


expected_answers = 1819125966, 1140
