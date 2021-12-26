#!/usr/bin/env python

import copy
import math

from . import read_data


def day18():
    CONTINUE = 'continue'
    EXPLODE = 'explode'
    SPLIT = 'split'
    DEBUG = False

    global changed_element
    changed_element = None

    def debug(*args):
        if DEBUG:
            print(*args)

    def add(snail, fish):
        return copy.deepcopy([snail, fish])

    def add_to_first(snail, value):
        """ Add value to the first (left most) number, and return the snail. """
        if type(snail) == int:
            return snail + value
        else:
            snail[0] = add_to_first(snail[0], value)
            return snail

    def add_to_last(snail, value):
        """ Add value to the last (right most) number, and return the snail. """
        if type(snail) == int:
            return snail + value
        else:
            snail[1] = add_to_last(snail[1], value)
            return snail

    def sub_reduce(snail, depth, split):
        """
        Traverse the snail and explode or split once.

         The first element of the return is the code indicating what happened:
            - CONTINUE: The snail pair was already reduced.
            - EXPLOSION: A pair exploded.  'left' and 'right' return elements are the values (if any) that need to be
                         added to the left and right elements of the outer scope.
            - SPLIT: A number was split into a pair.

        :param snail: The snail pair to walk.
        :param depth: The outer depth.
        :return: tuple(code, left, right)
        """

        global changed_element
        assert len(snail) == 2
        for rside in [0, 1]:
            # Explode.
            if type(snail[rside]) == list and depth >= 4:
                assert not split
                changed_element = copy.deepcopy(snail[rside])
                left, right = snail[rside]
                snail[rside] = 0
                # Update the other side of this pair.
                if not rside:
                    snail[1] = add_to_first(snail[1], right)
                    # Clear the side variable which was just handled already.
                    right = None
                else:
                    snail[0] = add_to_last(snail[0], left)
                    left = None
                return (EXPLODE, left, right)

            # Split.
            if split and type(snail[rside]) == int and snail[rside] >= 10:
                changed_element = snail[rside]
                number = snail[rside]
                snail[rside] = [math.floor(number/2), math.ceil(number/2)]
                return (SPLIT, None, None)

            # Depth first recursion before doing anything with the second element.
            if type(snail[rside]) == list:
                code, left, right = sub_reduce(snail[rside], depth=depth+1, split=split)
                if code == EXPLODE:
                    if not rside and right:
                        # We are on the left of a pair and have data for the right, so add it now.
                        snail[1] = add_to_first(snail[1], right)
                        right = None
                    if rside and left:
                        # We are on the right of a pair and have data for the left, so add it now.
                        snail[0] = add_to_last(snail[0], left)
                        left = None
                if code != CONTINUE:
                    return code, left, right

        # Made it all the way to the end.
        return CONTINUE, None, None

    def reduce(snail):
        """ Reduce the snail and return it. """
        debug(snail)
        split = False
        while True:
            code, _, _ = sub_reduce(snail, depth=1, split=split)
            # Left and right get thrown away if they reached it all the way back here.
            if code in [EXPLODE, SPLIT]:
                debug(snail, f" <- After {code} of {changed_element}")
            if code in [EXPLODE]:
                continue
            elif not split:
                assert code == CONTINUE
                # No more explosions.  Switch to splits.
                split = True
                continue
            elif split and code == SPLIT:
                # Did a split, so we need to check for explosions.
                split = False
                continue

            assert code == CONTINUE
            # No explosion or split, so we're done.
            return snail

    def magnitude(snail):
        """ Calculate and return the magnitude of a snailfish. """
        if type(snail) == int:
            return snail
        # Must be a pair now.
        left, right = snail
        return 3*magnitude(left) + 2*magnitude(right)

    lines = read_data('day18.data')
    sea = []
    for line in lines:
        sea.append(eval(line))

    snail = copy.deepcopy(sea[0])
    for fish in copy.deepcopy(sea[1:]):
        snail = add(snail, fish)
        snail = reduce(snail)

    print(f"Answer for day 18 part 1: {magnitude(snail)}")

    best = 0
    for snail in sea:
        for fish in sea:
            snailfish = reduce(add(snail, fish))
            mag = magnitude(snailfish)
            best = max(best, mag)
    print(f"Answer for day 18 part 2: {best}")

def main():
    day18()