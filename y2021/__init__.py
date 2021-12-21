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