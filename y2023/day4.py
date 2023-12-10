#!/usr/bin/env python

from AdventOfCode import read_data


def both_parts(data):
    """
    Part 1:
    Calculate the 'points' for all lottery cards, where a card's points start at 1 for one win and double for every
    additional win.

    Part2:
    Each win on a lottery card wins additional cards: one each of the next n cards, where n is the number of wins.

    :param data: The list of cards.
    :return: Tuple of the sum of card points and the total number of cards.
    """
    total_points = 0
    cards = {}

    for line in data:
        game, rest = line.split(':')
        game_id = int(game.split()[1])
        winning, mine = rest.split('|')
        # Convert to sets.
        winning = set(winning.split())
        mine = set(mine.split())
        wins = len(winning.intersection(mine))

        # Part 1.
        if wins:
            points = 2**(wins - 1)
            total_points += points

        # Part 2.
        cards[game_id] = cards.get(game_id, 0) + 1
        for win in range(1, wins+1):
            cards[game_id+win] = cards.get(game_id+win, 0) + cards[game_id]

    return total_points, sum(cards.values())


def main():
    data = read_data()
    return both_parts(data)


expected_answers = 21088, 6874754
