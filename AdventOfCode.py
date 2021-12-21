#!/usr/bin/env python

import pathlib
import sys
from time import time

sys.path.insert(1, pathlib.Path(__name__).parent)

import y2021


def main():
    y2021.day20.main()


if __name__ == '__main__':
    t0_all = time()
    main()
    print(f"Total time: {time() - t0_all:0.3f} seconds.")