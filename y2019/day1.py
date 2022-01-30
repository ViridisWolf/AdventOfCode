#!/usr/bin/env python

from . import read_data


def part1():
    """ Calculate fuel needed for each module. """
    fuel = 0

    lines = read_data('day1.data')
    for line in lines:
        module_mass = int(line.strip())
        assert module_mass//2 >= 0
        fuel += (module_mass//3) - 2

    print(f"Answer for 2015 day 1 part 1: {fuel}")


def part2():
    """ Calculate the needed fuel for each module, plus fuel for that fuel. """

    fuel = 0

    lines = read_data('day1.data')
    for line in lines:
        module_mass = int(line.strip())
        assert module_mass//2 >= 0
        fuel_add = (module_mass//3) - 2
        while fuel_add > 0:
            fuel += fuel_add
            fuel_add = (fuel_add//3) - 2

    print(f"Answer for 2015 day 1 part 2: {fuel}")


def main():
    """ Rocket equation type calculations. """
    part1()
    part2()

