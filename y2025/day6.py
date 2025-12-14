#!/usr/bin/env python
from AdventOfCode import read_data


def solve_problems(problems):
    """Return the sum of all the problems.

    The problem argument is a list of problems, where each problem has the
    operation as the first item and operands as subsequent items.
    """
    total = 0
    for problem in problems:
        operation, operands = problem[0], problem[1:]
        value = int(operands[0])
        for op in operands[1:]:
            if operation == '+':
                value += int(op)
            else:
                value *= int(op)
        total += value
    return total


def part1(lines):
    """
    The input is a series of math problems, with each problem being separated by a column of spaces.
    Part 1: Return the sum of the solutions of those math problems.
    """
    problems = [[] for _ in range(len(lines[0].split()))]
    for line in reversed(lines):
        row = line.split()
        for col, cell in enumerate(row):
            problems[col].append(cell)

    return solve_problems(problems)


def part2(lines):
    """
    The input is a series of math problems, with each problem being separated by a column of spaces.
    Part 2: the numbers in each math problem are to be read top-to-bottom instead of left-to-right. Return the sum of
            the solutions.
    """
    # Note: Be careful with the puzzle intput/data formatting.  Trailing spaces are important, but some code editors
    #       (like PyCharm) will trim trailing whitespace.  Create the data files with a more general-purpose editor.
    problems = [[]]
    for column in zip(*lines):
        line = ''.join(column[:-1]).strip()
        if not line:
            problems.append([])
        else:
            operation = column[-1].strip()
            if operation:
                problems[-1].append(operation)
            problems[-1].append(int(line))

    return solve_problems(problems)


def main():
    lines = read_data()
    return part1(lines), part2(lines)


expected_answers = 3968933219902, 6019576291014
