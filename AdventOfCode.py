#!/usr/bin/env python

import argparse
import importlib
import pathlib
import time


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


def get_years():
    """ Returns a list of available year numbers as strings. """
    years = []
    p = pathlib.Path(__file__).parent
    for year in p.glob('y*/'):
        year = year.name[1:]
        if year.isnumeric():
            years.append(year)
    assert years, f"No years found!"
    return years


def get_days(year):
    """ Returns a list of available days as strings of numbers for the specified year. """

    days = []
    p = pathlib.Path(__file__).parent
    for day in p.glob(f'y{year}/day*.py'):
        day = day.name[3:-3]
        if day.isnumeric():
            days.append(day)
    assert days, f"No days found for year {year}!"
    days.sort(key=lambda x: int(x))
    return days


def get_day_module(year, day):
    """ Return the module for the specified year and day. """
    return importlib.import_module(f'y{year}.day{day}')


def main(year=None, day=None):
    if year:
        years = [year]
    else:
        years = get_years()

    for year in years:
        if day:
            days = [day]
        else:
            days = get_days(year)

        for d in days:
            module = get_day_module(year, d)
            runtime(module.main)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="The AoC year.")
    parser.add_argument('--day', type=int, help="The AoC day.")
    args = parser.parse_args()

    t0_all = time.time()
    main(args.year, args.day)
    print(f"Total time: {time.time() - t0_all:0.3f} seconds.")
