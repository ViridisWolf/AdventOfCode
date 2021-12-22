#!/usr/bin/env python

import pathlib
import sys
import time

sys.path.insert(1, pathlib.Path(__name__).parent)

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


def main():
    runtime(y2021.day19.main)
    runtime(y2021.day20.main)
    runtime(y2021.day21.main)


if __name__ == '__main__':
    t0_all = time.time()
    main()
    print(f"Total time: {time.time() - t0_all:0.3f} seconds.")