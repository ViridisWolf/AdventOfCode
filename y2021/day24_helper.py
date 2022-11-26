#!/usr/bin/env python

import random
import re
from pprint import pprint

from . import read_data


def model_check_orig(model_number):
    # Convert puzzle input to Python code for easier reading.
    lines = read_data('day24.data')
    index = 0
    instructions = []
    for line in lines:
        if line.startswith('inp'):
            line = re.sub(r'inp (\w)', fr'\1 = m[{index}]', line)
            index += 1
        line = re.sub(r'add (\w) (\w|-?\d+)', r'\1 = \1 + \2', line)
        line = re.sub(r'mul (\w) (\w|-?\d+)', r'\1 = \1 * \2', line)
        line = re.sub(r'div (\w) (\w|-?\d+)', r'\1 = \1 // \2', line)
        line = re.sub(r'mod (\w) (\w|-?\d+)', r'\1 = \1 % \2', line)
        line = re.sub(r'eql (\w) (\w|-?\d+)', r'\1 = 1 if \1 == \2 else 0', line)
        instructions.append(line)
    # Run the converted code.
    var = {'w': 0, 'x': 0, 'y': 0, 'z': 0, 'm': model_number}
    for inst in instructions:
        # Exec is very slow.
        # Runtime would be much faster to have exec create a function and thus only call exec once, or print the
        # converted code and create a function manually.
        exec(inst, globals(), var)
    return var['z']


def model_check_simple(m):
    """ Input is a string or list. """
    w, x, y, z = 0, 0, 0, 0
    z = m[0] + 9
    y = 26
    z *= y
    y = m[1] + 4
    z += y
    x = 1
    y = 26
    z *= y
    y = m[2] + 2
    y *= x
    z += y
    x = z
    x = x % 26
    z = z // 26
    x += -9
    x = 1 if x != m[3] else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = m[3] + 5
    y *= x
    z += y
    x = z
    x = x % 26
    z = z // 26
    x += -9
    x = 1 if x != m[4] else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = m[4] + 1
    y *= x
    z += y
    x = 1
    y = 26
    z *= y
    y = m[5] + 6
    y *= x
    z += y
    x = 1
    y = 26
    z *= y
    y = m[6] + 11
    y *= x
    z += y
    x = z
    x = x % 26
    z = z // 26
    x += -10
    x = 1 if x != m[7] else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = m[7] + 15
    y *= x
    z += y
    x = 1
    y = 26
    z *= y
    y = m[8] + 7
    y *= x
    z += y
    x = z
    x = x % 26
    z = z // 26
    x += -2
    x = 1 if x != m[9] else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = m[9] + 12
    y *= x
    z += y
    x = 1
    y = 26
    z *= y
    y = m[10] + 15
    y *= x
    z += y
    x = z
    x = x % 26
    z = z // 26
    x += -15
    x = 1 if x != m[11] else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = m[11] + 9
    y *= x
    z += y
    x = z
    x = x % 26
    z = z // 26
    x += -9
    x = 1 if x != m[12] else 0
    y = 25
    y *= x
    y += 1
    z *= y
    y = m[12] + 12
    y *= x
    z += y
    x = z
    x = x % 26
    z = z // 26
    x += -3
    x = 1 if x != m[13] else 0
    y = 25*x + 1
    z *= y
    y = m[13] + 12
    y *= x
    z += y
    return z


def main():
    n = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    for _ in range(100):
        m = []
        for i in range(14):
            m.append(random.choice(n))
        z = model_check_orig(m)

        assert model_check_simple(m) == z

    print(model_check_orig([3, 9, 9, 2, 4, 9, 8, 9, 4, 9, 9, 9, 6, 9]))  # 39924989499969
    print(model_check_orig([1, 6, 8, 1, 1, 4, 1, 2, 1, 6, 1, 1, 1, 7]))  # 16811412161117
