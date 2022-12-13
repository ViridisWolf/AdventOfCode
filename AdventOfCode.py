#!/usr/bin/env python

import argparse
import importlib
import pathlib
import time


def read_data(caller, filename=None):
    """
    Read the specified input data file and strip any extra white space from each line.

    :param caller: The path of the caller, e.g. __file__.
    :param filename: The name of the data file, or None to use the format of "day#.txt".
    :return: List of line strings.
    """
    if filename is None:
        filename = pathlib.Path(caller).stem + '.txt'
    datafile = pathlib.Path(caller).parent / 'data' / filename
    with open(datafile, 'r') as f:
        lines = f.readlines()
    lines = [line.strip('\n\r') for line in lines]
    return lines


def run_and_check(module, args):
    """
    Runs the main function, prints the results, and checks them against the expected values.

    :param module: The module which has main().
    :param args: The args object, which must have correct values in .year and .day.
    :return: The number of answers which did not match the expected value.
    """

    count_wrong = 0

    results = module.main()
    if results is None:
        # Assume that the module is printing the answers itself.
        assert not args.check, f"{module.__name__} is not setup for result checking!"
        return count_wrong

    for part, answer in enumerate(results, 1):
        if type(answer) is str and '\n' in answer:
            # Make sure that any multiline answer starts on a new line.
            print(f"Answer for {args.year} day {args.day} part {part}:\n{answer}", end='')
        else:
            print(f"Answer for {args.year} day {args.day} part {part}: {answer}", end='')
        if not args.check:
            print()
            continue

        expected_answer = module.expected_answers[part - 1]
        if answer == expected_answer:
            print()
            continue

        count_wrong += 1
        if type(expected_answer) is str and '\n' in expected_answer:
            # Make sure that any multiline answer starts on a new line.
            print(f"\n ^^^ Wrong answer!  Expected:\n{expected_answer}")
        else:
            print(f"  <-- Wrong answer!  Expected {expected_answer}.")

    return count_wrong


def runtime(module, args=None):
    """
    Display the runtime of the specified function.
    :param module: The module with main() to call.
    :return: Return value from run_and_check().
    """

    t0 = time.perf_counter()
    result = run_and_check(module, args=args)
    t1 = time.perf_counter()
    print(f"^^^ ran in {t1-t0:0.3f} seconds ^^^")
    return result


def get_years():
    """ Returns a list of available year numbers as strings. """
    years = []
    p = pathlib.Path(__file__).parent
    for year in p.glob('y*/'):
        year = year.name[1:]
        if year.isnumeric():
            years.append(year)
    assert years, f"No years found!"
    years.sort(key=lambda x: int(x))
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


def main(year=None, day=None, args=None):
    wrong_count = 0

    if year:
        years = [year]
    else:
        years = get_years()

    for year in years:
        args.year = year
        if day:
            days = [day]
        else:
            days = get_days(year)

        for d in days:
            args.day = d
            module = get_day_module(year, d)
            wrong_count += runtime(module, args=args)
    return wrong_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="The AoC year.")
    parser.add_argument('--day', type=int, help="The AoC day.")
    parser.add_argument('--check', action='store_true', help="Check that each result matches expectation.")
    args = parser.parse_args()

    t0_all = time.perf_counter()
    result = main(args.year, args.day, args)
    print(f"Total time: {time.perf_counter() - t0_all:0.3f} seconds.")
    if result:
        print(f"Failure: {result} answers were wrong.")
