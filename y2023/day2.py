#!/usr/bin/env python

from AdventOfCode import read_data


def both_parts(data):
    """
    Figure out which dice games are possible with the specified dice count, and also what the "power" of each game is.
    The power is the product of the minimum number of dice of each color required for that game.

    :param data: The puzzle input data as a list of strings.
    :return: A tuple of the answers for part1 and part2.
    """

    dice_available = {'red': 12, 'green': 13, 'blue': 14}
    possible_sum = 0
    power_sum = 0

    for game_str in data:
        dice_required = {'red': 0, 'green': 0, 'blue': 0}

        game_id, dice = game_str.removeprefix('Game ').split(':')
        for die_str in dice.replace(';', ',').split(','):
            amount, color = die_str.strip().split(' ')
            amount = int(amount)
            dice_required[color] = max(dice_required[color], amount)

        if all([dice_required[color] <= dice_available[color] for color in dice_available]):
            possible_sum += int(game_id)
        power_sum += dice_required['red'] * dice_required['blue'] * dice_required['green']

    return possible_sum, power_sum


# def part1_orig(data):
#     color_max = {'red': 12, 'green': 13, 'blue': 14}
#     possible_sum = 0
#
#     for line in data:
#         possible = True
#         game, other = line.split(':')
#         game_id = int(game.split(' ')[1])
#         for color_str in other.replace(';', ',').split(','):
#             amount, color = color_str.strip().split(' ')
#             amount = int(amount)
#             if amount > color_max[color]:
#                 # Game is not possible.
#                 possible = False
#                 break
#         if possible is True:
#             possible_sum += game_id
#
#     return possible_sum
#
#
# def part2_orig(data):
#     total_power = 1
#
#     for line in data:
#         game, other = line.split(':')
#         game_mins = {'red': 0, 'green': 0, 'blue': 0}
#
#         for color_str in other.replace(';', ',').split(','):
#             amount, color = color_str.strip().split(' ')
#             amount = int(amount)
#             game_mins[color] = max(game_mins[color], amount)
#
#         power = game_mins['red'] * game_mins['blue'] * game_mins['green']
#         total_power += power
#
#     return total_power


def main():
    data = read_data(__file__)
    return both_parts(data)


expected_answers = 2593, 54699
