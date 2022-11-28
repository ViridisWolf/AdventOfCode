#!/usr/bin/env python

import statistics

from AdventOfCode import read_data

corrupted_points_table = {')': 3, ']': 57, '}': 1197, '>': 25137}
missing_points_table = {')': 1, ']': 2, '}': 3, '>': 4}
opening_to_closing = {'(': ')', '[': ']', '{': '}', '<': '>'}
closing_to_opening = {v: k for k, v in opening_to_closing.items()}


def day10():
    corrupted_characters = []
    missing_scores = []

    lines = read_data(__file__)
    for line in lines:
        corrupted = False
        stack = []
        for char in line:
            if char in '([{<':
                stack.append(char)
            elif char in ')]}>':
                expected = opening_to_closing[stack.pop()]
                if char != expected:
                    corrupted = True
                    corrupted_characters.append(char)
            else:
                raise AssertionError

        if stack and not corrupted:
            score = 0
            # print(f"Incomplete line: {line}, with these unmatched: {stack}")
            for char in reversed(stack):
                missing = opening_to_closing[char]
                score *= 5
                score += missing_points_table[missing]
            missing_scores.append(score)

    score = 0
    for char in corrupted_characters:
        score += corrupted_points_table[char]
    print(f"Answer for 2021 day 10 part 1: {score}")

    score = statistics.median(missing_scores)
    print(f"Answer for 2021 day 10 part 2: {score}")


def main():
    day10()
