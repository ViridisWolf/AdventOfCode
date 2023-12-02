#!/usr/bin/env python

import argparse
import concurrent.futures
import importlib
import os
import pathlib
import pdb
import sys
import time
import traceback


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


def run_and_check(module, year, day, check=False):
    """
    Runs the main function, checks the results against the expected values, and returns the results.

    :param module: The module which has main().
    :param year: The year to display.
    :param day: The day to display.
    :param check: Whether to check the answer.
    :return: The number of answers which did not match the expected value, and a string of the output.
    """

    count_wrong = 0
    ret_string = ""

    results = module.main()
    if results is None:
        # Assume that the module is printing the answers itself.
        assert not check, f"{module.__name__} is not setup for result checking!"
        return count_wrong

    for part, answer in enumerate(results, 1):
        if type(answer) is str and '\n' in answer:
            # Make sure that any multiline answer starts on a new line.
            ret_string += f"Answer for {year} day {day} part {part}:\n{answer}"
        else:
            ret_string += f"Answer for {year} day {day} part {part}: {answer}"
        if not check:
            ret_string += '\n'
            continue

        expected_answer = module.expected_answers[part - 1]
        if answer == expected_answer:
            ret_string += '\n'
            continue

        count_wrong += 1
        if type(expected_answer) is str and '\n' in expected_answer:
            # Make sure that any multiline answer starts on a new line.
            ret_string += f"\n ^^^ Wrong answer!  Expected:\n{expected_answer}\n"
        else:
            ret_string += f"  <-- Wrong answer!  Expected {expected_answer}.\n"

    return count_wrong, ret_string


def runtime(args):
    """
    Import and run the puzzle module.  Adds run duration info to the result string.

    :param args: Tuple containing the year, day, check, and samples variables.
    :return: 2-tuple of the error count and the result string.
    """

    year, day, check, samples = args
    assert samples >= 1

    module = get_day_module(year, day)

    t0 = time.perf_counter()
    for _ in range(samples):
        errors, ret_string = run_and_check(module, year, day, check)
    t1 = time.perf_counter()
    ret_string += f"^^^ ran in {(t1-t0)/samples:0.3f} seconds {'average ' if samples > 1 else ''}^^^"
    return errors, ret_string


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


def run_all(days, args):
    """
    Collect answers for all specified puzzle days, print the answers, and return how many were wrong.
    This may use multithreading.

    :param days: Sequence of input arguments to the runtime function for each puzzle solution.
    :param args: The Argument Parser result, which must have .threads.
    :return: The count of wrong answers.
    """
    errors = 0

    with concurrent.futures.ProcessPoolExecutor(max(1, args.threads)) as pool:
        if args.threads > 1 and len(days) > 1:
            results = pool.map(runtime, days)
        else:
            results = map(runtime, days)

        for answer_errors, answer_string in results:
            errors += answer_errors
            print(answer_string)

    return errors


def exception_handler(typ, value, tb):
    if not sys.stderr.isatty() or not sys.stdout.isatty():
        # If this isn't a tty-like device, then just fallback to the default hook.
        sys.__excepthook__(typ, value, tb)
    else:
        traceback.print_exception(typ, value, tb)
        pdb.pm()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="The AoC year.")
    parser.add_argument('--day', type=int, help="The AoC day.")
    parser.add_argument('--check', action='store_true', help="Check that each result matches expectation.")
    parser.add_argument('--samples', type=int, default=1, help="Sample count to take for a solution's runtime.")
    parser.add_argument('--threads', type=int, default=os.cpu_count(), help="Number of compute threads to use.")
    parser.add_argument('--pdb', action='store_true', help="Drop into PDB when there is an unhandled exception.")
    args = parser.parse_args()

    if args.pdb:
        sys.excepthook = exception_handler

    years = [args.year] if args.year else get_years()
    puzzle_list = [(y, d, args.check, args.samples)
                   for y in years
                   for d in ([args.day] if args.day else get_days(y))]

    t0_all = time.perf_counter()
    result = run_all(puzzle_list, args)
    print(f"Total time: {time.perf_counter() - t0_all:0.3f} seconds.")
    if result:
        print(f"Failure: {result} answers were wrong.")


if __name__ == '__main__':
    sys.exit(main())
