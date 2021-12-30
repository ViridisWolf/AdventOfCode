#!/usr/bin/env python

import argparse
import pathlib
import sys
import time

sys.path.insert(1, pathlib.Path(__name__).parent)

import y2015
import y2021


def runtime(func, args=()):
    """
    Display the runtime of the specified function.
    :param func: function to run.
    :param args: Args to be passed to that function.
    :return: None.
    """

    t0 = time.time()
    result = func(*args)
    t1 = time.time()
    print(f"^^^ ran in {t1-t0:0.3f} seconds ^^^")


def main(year=None, day=None):

    years = {
            2015: y2015,
            2021: y2021,
            }

    # Run each year.
    if year is not None:
        years = {year: years[year]}
    for y in years.values():
        days = y.get_days()

        # Run each day function for this year.
        if day is not None:
            days = {day: days[day]}
        for day in days.values():
            runtime(day)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="The AoC year.")
    parser.add_argument('--day', type=int, help="The AoC day.")
    args = parser.parse_args()

    t0_all = time.time()
    main(args.year, args.day)
    print(f"Total time: {time.time() - t0_all:0.3f} seconds.")