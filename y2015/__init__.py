#!/usr/bin/env python

from pathlib import Path


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
