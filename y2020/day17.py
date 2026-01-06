#!/usr/bin/env python
from dataclasses import dataclass
from functools import cache

from AdventOfCode import read_data


@dataclass(frozen=True)
class Cell:
    """A cube in 3D or 4D space."""
    x: int
    y: int
    z: int
    w: int = None

    @cache
    def get_neighbors(self):
        """Return all neighbors of this cell."""
        neighbors = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                for z in range(self.z - 1, self.z + 2):
                    for w in ([None] if self.w is None else range(self.w - 1, self.w + 2)):
                        if x != self.x or y != self.y or z != self.z or w != self.w:
                            neighbors.append(self.__class__(x, y, z, w))
        return tuple(neighbors)

    def next_state(self, active, active_cells):
        """Return True if this cell will be active for the next tick."""
        neighbors = 0
        for neighbor in self.get_neighbors():
            if neighbor in active_cells:
                neighbors += 1

        if active and neighbors in [2, 3]:
            return True
        if neighbors == 3:
            return True
        return False


def parts(lines, part=1):
    """
    Calculate how many cells/cubes are active after 6 cycles/ticks.

    Part 1: 3D space.
    Part 2: 4D space.
    """
    active_cells = set()
    w = None if part==1 else 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                cell = Cell(x, y, 0, w)
                active_cells.add(cell)

    for tick in range(6):
        inactive_cells = set([n for cell in active_cells for n in cell.get_neighbors() if n not in active_cells])
        next_cells = set(cell for cell in inactive_cells if cell.next_state(False, active_cells))
        next_cells.update(cell for cell in active_cells if cell.next_state(True, active_cells))
        active_cells = next_cells

    return len(active_cells)


def main():
    lines = read_data()
    return parts(lines), parts(lines, part=2)


expected_answers = 338, 2440
