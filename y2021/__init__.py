#!/usr/bin/env python

from pathlib import Path

__all__ = []
scripts = Path(Path(__file__).parent).glob('*.py')
for script in scripts:
    if script.name == '__init__.py':
        continue
    if script.is_file():
        __all__.append(script.stem)

# "import *" uses the __all__ variable.
from . import *


def get_days():
    """ Return a list of the main functions for each day in this year. """

    days = {
        1: day1.main,
        2: day2.main,
        3: day3.main,
        19: day19.main,
        20: day20.main,
        21: day21.main,
        22: day22.main,
        23: day23.main,
        }
    return days
