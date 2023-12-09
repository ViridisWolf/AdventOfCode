#!/usr/bin/env python

from functools import cmp_to_key

from AdventOfCode import read_data


def max_count(hand):
    count = 0
    max_card = None
    for card in hand:
        new_count = hand.count(card)
        if new_count > count:
            count = new_count
            max_card = card
    return count, max_card, hand


def max_count_wild(hand):
    score = max_count(hand)
    for card in "23456789TQKA":
        tmp_hand = hand.replace('J', card)
        score = max(score, max_count(tmp_hand))
    return score


def get_type(hand):
    """
    Return the poker-ish type of the hand.

    :param hand: the hand, as a string.
    :return: A number representing the type of hand:
        The type of hand as an integer:
            1   - single card
            2   - single pair
            2.5 - two pair
            3   - three of a kind
            3.5 - full house
            4   - four of a kind
            5   - five of a kind
    """
    if card_value['J'] == 11 or 'J' not in hand:
        count, card, hand = max_count(hand)
    else:
        count, card, hand = max_count_wild(hand)

    if count == 3:
        hand = hand.replace(card, '')
        if hand[0] == hand[1]:
            return 3.5
    elif count == 2:
        if len(set(hand)) == 3:
            # If there is nothing more than a pair but have only 3 different cards, then that must be two pair.
            return 2.5

    return count


card_value = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def greater_than(first, second):
    """
    Return 1 if the first hand has a higher score than the second, 0 if they are equal, and -1 if the second is higher.

    :param first: The first hand, as a string.
    :param second: The second hand, as a string.
    """

    global card_value

    greater = 0
    first_type = get_type(first)
    second_type = get_type(second)
    if first_type > second_type:
        return 1
    elif first_type < second_type:
        return -1

    for card1, card2 in zip(first, second):
        if card_value[card1] != card_value[card2]:
            greater = card_value[card1] > card_value[card2]
            if greater is True:
                return 1
            else:
                return -1

    assert first == second
    return greater


def day7(data, part):
    """
    Rank "Camel Card" hands, which are first ranked by poker hands and then by individual card values in the original
    card order.

    Part 1: 'J' cards are jacks, ranked between tens and queens.
    Part 2: 'J' cards are wild jokers, ranked lower than any other card.
    """

    global card_value

    if part == 1:
        # This global dictionary is also checked later to infer which part is being done.
        card_value['J'] = 11
    else:
        card_value['J'] = 1

    hands = []
    bids = {}
    for line in data:
        hand, bid = line.split()
        hands.append(hand)
        bids[hand] = int(bid)
    hands = sorted(hands, key=cmp_to_key(greater_than))

    total_winnings = 0
    for rank, hand in enumerate(hands, start=1):
        bid = bids[hand]
        total_winnings += rank * bid

    return total_winnings


def main():
    data = read_data(__file__)
    answer1 = day7(data, part=1)
    answer2 = day7(data, part=2)
    return answer1, answer2


expected_answers = 251136060, 249400220
