#!/usr/bin/env python

from collections import namedtuple

from AdventOfCode import read_data

def day13(silent=False):
    class Paper:
        Point = namedtuple("Point", "x y")

        def __init__(self):
            self.points = set()
            self.max_x = 0
            self.max_y = 0

        def mark(self, x, y):
            """
            Mark a dot in a specified cell.

            :param x: The column number, zero based from left.
            :param y: The row number, zero based from top.
            :return:
            """
            x, y = int(x), int(y)
            assert x >= 0 and y >= 0
            dot = self.Point(x, y)
            self.points.add(dot)
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

        def count(self):
            """
            Returns the number of dots visible on the paper.

            :return (int): The count of dots.
            """

            return len(self.points)

        def fold(self, x=None, y=None):
            assert (x is not None) ^ (y is not None), "Must specify x or y, but not both."
            x = x if x is not None else self.max_x
            y = y if y is not None else self.max_y

            for dot in self.points.copy():
                if dot.x > x:
                    # Do the fold.
                    self.points.remove(dot)
                    self.mark(x - (dot.x - x), dot.y)
                elif dot.y > y:
                    self.points.remove(dot)
                    self.mark(dot.x, y - (dot.y - y))

        def print(self, glyph='█'):
            text = ""
            rows = []
            for dot in self.points:
                # Construct the ouput table.
                if len(rows) <= dot.y:
                    rows += [None]*(dot.y + 1 - len(rows))
                if rows[dot.y] is None:
                    rows[dot.y] = []
                row = rows[dot.y]
                if len(row) <= dot.x:
                    row += [' ']*(dot.x + 1 - len(row))
                row[dot.x] = glyph

            rows = ['' if row is None else ''.join(row) for row in rows]
            return '\n'.join(rows)

    # Done defining things.  Start doing.
    folds = []
    paper = Paper()

    lines = read_data(__file__)

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if 'fold along ' in line:
            param = line[11]
            assert param in ['x', 'y']
            position = int(line[13:])
            folds += [(param, position)]
        elif ',' in line:
            x, y = line.split(',')
            paper.mark(x, y)

    for count, fold in enumerate(folds):
        if count == 1:
            # print(f"Answer for 2021 day 13 part 1: {paper.count()}")
            answer1 = paper.count()
        # print(f"{paper.count()} dots before fold {fold}", end='')
        x, y = None, None
        assert fold[0] in ['x', 'y']
        if fold[0] == 'x':
            x = fold[1]
        else:
            y = fold[1]
        paper.fold(x, y)
        # print(f" and {paper.count()} after.")
    if not silent:
        print(paper.print())

    answer2 = paper.print()
    return answer1, answer2


def main():
    return day13(silent=True)


expected_answers = (710,
                    "████ ███  █     ██  ███  █  █ █    ███\n"
                    "█    █  █ █    █  █ █  █ █  █ █    █  █\n"
                    "███  █  █ █    █    █  █ █  █ █    █  █\n"
                    "█    ███  █    █ ██ ███  █  █ █    ███\n"
                    "█    █    █    █  █ █ █  █  █ █    █ █\n"
                    "████ █    ████  ███ █  █  ██  ████ █  █")
