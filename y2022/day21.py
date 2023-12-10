#!/usr/bin/env python

from AdventOfCode import read_data


def day(data, part):
    """
    There are many monkeys (the input).  Each will either yell a constant number or will yell the
    result of a mathematical operation performed on what two other monkeys yelled.

    Part1: Calculate what 'root' will yell.
    Part2: Calculate what 'humn' should yell to get the two values looked at by 'root' to be equal.
    """
    monkeys = {}
    monkeys_ready = []
    goes_to = {}
    done = {}
    for line in data:
        name, yell = line.split(': ')
        monkeys[name] = yell
        if yell.isnumeric():
            monkeys[name] = yell
            monkeys_ready.append(name)
        else:
            from1, _, from2 = yell.split(' ')
            for from_monkey in [from1, from2]:
                if from_monkey not in goes_to:
                    goes_to[from_monkey] = []
                goes_to[from_monkey].append(name)

    # Part 2 changes to the puzzle input.
    if part == 2:
        monkeys['humn'] = 'x'
        monkeys['root'] = monkeys['root'].replace('+', '=')

    while monkeys_ready:
        monk = monkeys_ready.pop()
        for dependent in goes_to.get(monk, []):
            yell = monkeys[dependent].replace(monk, f"({monkeys[monk]})")
            monkeys[dependent] = yell
            done[dependent] = done.get(dependent, 0) + 1
            if done[dependent] == 2:
                # Evaluate and add to the constant monkeys.
                if 'x' not in yell:
                    yell = eval(yell)
                monkeys[dependent] = str(yell)
                monkeys_ready.append(dependent)

    if part == 1:
        return int(float(monkeys['root']))

    elif part == 2:
        yell = monkeys['root']
        left, right = yell.split('=')
        if 'x' in right:
            left, right = right, left
        left = f"{left} - {eval(right)}"

        # Do a binary search for the solution.
        x = 0
        if eval(left) > 0:
            # Assumption: x (the answer to part 2) will need to be a positive integer.
            # The search code below requires that 'left' has positive correlation with 'x', so swap if needed.
            left = f"-({left})"
        equation = eval(f"lambda x: {left}")

        x = 1
        while equation(x) < 0:
            x_min = x
            x *= 2
        x_max = x

        while True:
            result = equation(x)
            if result == 0:
                break
            elif result < 0:
                x_min = x
            else:
                x_max = x
            x = (x_min + x_max) // 2

        return x


def main():
    data = read_data()
    answer1 = day(data, part=1)
    answer2 = day(data, part=2)
    return answer1, answer2


expected_answers = 83056452926300, 3469704905529
