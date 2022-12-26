#!/usr/bin/env python3

row = 2978
column = 3083
starting = 20151125


def part1():
    x, y = column, row
    nth = x*(x+1)//2 + x*(y-1) + (y-2)*(y-1)//2
    number = starting

    # print(f"n = {nth}")
    # print(number)
    for _ in range(nth - 1):
        number = (number * 252533) % 33554393
        # print(number)

    # print(f"Answer for 2015 day 25 part 1: {number}")
    return number


def main():
    return part1(),


expected_answers = 2650453,
