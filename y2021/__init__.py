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
        19: day19.main,
        20: day20.main,
        21: day21.main,
        22: day22.main,
        }
    return days
