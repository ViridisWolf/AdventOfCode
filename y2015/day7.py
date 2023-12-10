#!/usr/bin/env python
import re
from functools import cache

from AdventOfCode import read_data


class Signals:
    _opcode = {
        None: lambda x: x,
        'NOT': lambda x: ~x,
        'AND': lambda x, y: x & y,
        'OR': lambda x, y: x | y,
        'LSHIFT': lambda x, y: x << y,
        'RSHIFT': lambda x, y: x >> y,
    }

    def __init__(self):
        self._signals = {}

    @staticmethod
    def parse_op_and_args(line):
        """ Return the operation string, and then the args as a list. """
        assert '->' not in line
        match = re.search('[A-Z]+', line)
        if match is None:
            op = None
            args = [line]
        else:
            op = match.group(0)
            args = line.replace(op, '').split()

        args = [int(a) if a.isdigit() else a for a in args]
        return op, args

    def add_signal(self, line):
        """ Parse an instruction line and add the signal definition to the list of known signals. """
        line, sig = line.split(' -> ')
        op, args = self.parse_op_and_args(line)
        self._signals[sig] = (self._opcode[op], args)

    @cache
    def get_signal(self, sig):
        """ Return the integer value of the specified signal caries. """
        op, args = self._signals[sig]
        final_args = []
        for arg in args:
            if isinstance(arg, int):
                pass
            elif arg.isdigit():
                arg = int(arg)
            else:
                arg = self.get_signal(arg)
            assert isinstance(arg, int)
            final_args.append(arg)

        value = op(*final_args)
        return value

    # def get_signal_alt(self, sig):
    #     """
    #     Return the integer value of the specified signal caries.
    #
    #     This function has the side effect of updating signal arguments to their computed integer values.
    #     """
    #     op, args = self._signals[sig]
    #     for index, arg in enumerate(args):
    #         if isinstance(arg, int):
    #             pass
    #         elif arg.isdigit():
    #             args[index] = int(arg)
    #         else:
    #             args[index] = self.get_signal(arg)
    #
    #     value = op(*args)
    #     return value

    def force_signal(self, sig, value):
        """ Force/override a signal so that it has the specified constant value. """
        self._signals[sig] = self._opcode[None], [value]


def main():
    data = read_data()

    signals = Signals()
    for line in data:
        signals.add_signal(line)

    # Part 1
    answer1 = signals.get_signal('a')

    # Part 2
    signals.get_signal.cache_clear()
    signals.force_signal('b', answer1)
    answer2 = signals.get_signal('a')

    return answer1, answer2


expected_answers = (3176, 14710)
