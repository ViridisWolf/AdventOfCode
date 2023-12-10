#!/usr/bin/env python

from AdventOfCode import read_data


class Elves:
    def __init__(self, data):
        self.starting_direction = 0
        self.rounds_done = 0
        # +x is right, +y is down.
        self.map = set()
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                if char == '#':
                    self.map.add((x, y))

    def neighbors(self, elf):
        """ Return a list of whether there are elves in the north, south, west, and east directions. """
        x, y = elf
        nw = (x-1, y-1) in self.map
        nn = (x  , y-1) in self.map
        ne = (x+1, y-1) in self.map
        ww = (x-1, y  ) in self.map
        ee = (x+1, y  ) in self.map
        sw = (x-1, y+1) in self.map
        ss = (x  , y+1) in self.map
        se = (x+1, y+1) in self.map
        directions = [(nn or ne or nw, (x  , y-1)),
                      (ss or se or sw, (x  , y+1)),
                      (ww or nw or sw, (x-1, y  )),
                      (ee or ne or se, (x+1, y  )),]

        # Rotate the directions so that they are in priority order.
        return directions[self.starting_direction:] + directions[:self.starting_direction]

    def propose_and_move(self):
        """ Propose moves and then do non-conflicting movement, and return whether any elf moved. """
        proposals = {}
        for elf in self.map:
            directions = self.neighbors(elf)
            if any(x[0] for x in directions):
                for elves_present, spot in directions:
                    if not elves_present:
                        if spot not in proposals:
                            proposals[spot] = elf
                        else:
                            proposals[spot] = None
                        break

        # Now move the elves.
        moved = False
        for location, elf in proposals.items():
            if elf is None:
                continue
            moved = True
            self.map.add(location)
            self.map.remove(elf)
        return moved

    def step(self):
        """ Do one iteration of elf movement, and return True if any elf moved. """
        moved = self.propose_and_move()
        # Update the starting direction for the next iteration.
        self.starting_direction = (self.starting_direction + 1) % 4
        self.rounds_done += 1
        return moved

    def get_rectangle(self):
        """Return the dimensions (x min/max, y min/max) for the smallest rectangle that covers all the elves. """
        x_min, y_min = next(iter(self.map))
        x_max, y_max = x_min, y_min

        for x, y in self.map:
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)
        return x_min, x_max, y_min, y_max

    def get_coverage(self):
        """ Return the number of empty spaces in the smallest rectangle that can be drawn around the elves. """
        x_min, x_max, y_min, y_max = self.get_rectangle()
        return ((x_max - x_min + 1) * (y_max - y_min + 1)) - len(self.map)

    def print(self):
        """ Print a map of all the elves. """
        x_min, x_max, y_min, y_max = self.get_rectangle()
        for y in range(y_min, y_max+1):
            line = ''
            for x in range(x_min, x_max+1):
                line += '#' if (x, y) in self.map else '.'
            print(line)


def day(data):
    """ Calculate the coverage score after 10 rounds, and how many rounds are needed (+1) to reach steady-state. """
    elf_map = Elves(data)

    for _ in range(10):
        elf_map.step()
    answer1 = elf_map.get_coverage()

    while elf_map.step() is True:
        pass
    answer2 = elf_map.rounds_done

    return answer1, answer2


def main():
    data = read_data()
    answer1, answer2 = day(data)
    return answer1, answer2


expected_answers = 3947, 1012
