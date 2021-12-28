#!/usr/bin/env python

from pathlib import Path

__all__ = []
scripts = Path(Path(__file__).parent).glob('*.py')
for script in scripts:
    if script.name == '__init__.py':
        continue
    if script.is_file():
        __all__.append(script.stem)


def read_data(filename):
    """
    Read the specified input data file and strip any extra white space from each line.

    :param filename: The name of the data file.
    :return: List of lines strings.
    """
    datafile = Path(__file__).parent / 'data' / filename
    with open(datafile, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


# "import *" uses the __all__ variable.
from . import *


def get_days():
    """ Return a list of the main functions for each day in this year. """

    days = {
        1: day1.main,
        2: day2.main,
        3: day3.main,
        4: day4.main,
        5: day5.main,
        6: day6.main,
        7: day7.main,
        8: day8.main,
        9: day9.main,
        10: day10.main,
        13: day13.main,
        14: day14.main,
        15: day15.main,
        16: day16.main,
        17: day17.main,
        18: day18.main,
        19: day19.main,
        20: day20.main,
        21: day21.main,
        22: day22.main,
        23: day23.main,
        # 24: day24.main, # Day 24 was solved mostly by hand. The day24.py file exists, but only has some helper code.
        25: day25.main,
        }
    return days


