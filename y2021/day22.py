#!/usr/bin/env python

from . import read_data


DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


def part2(max_size=None, part=2):
    def get_size(cuboid):
        """ Return the number of cubes in the cuboid. """
        cx, cy, cz = cuboid
        return (cx[1]-cx[0]+1) * (cy[1]-cy[0]+1) * (cz[1]-cz[0]+1)

    def shrink(top, layers, all=False):
        """ Shrink the next intersecting layer down to the portion that overlaps with top."""
        if not layers:
            return ()
        cx, cy, cz = top[1]
        shrunks = []
        for index, layer in enumerate(layers):
            lx, ly, lz = layer[1]
            if (       lx[0] > cx[1] or ly[0] > cy[1] or lz[0] > cz[1]
                    or lx[1] < cx[0] or ly[1] < cy[0] or lz[1] < cz[0]):
                # This layer doesn't overlap, so skip it.
                continue
            shrinkydink = (max(lx[0], cx[0]), min(lx[1], cx[1])),\
                          (max(ly[0], cy[0]), min(ly[1], cy[1])),\
                          (max(lz[0], cz[0]), min(lz[1], cz[1]))
            debug("Shrunk layer to", shrinkydink)
            shrunks.append((layer[0], shrinkydink))
            if len(shrunks) >= 2 and not all:
                break
        return tuple(shrunks) + layers[index+1:]

    def split_at(cuboid, x=None, y=None, z=None):
        """
        Create two cuboids by splitting input cuboid at the specified place.
        The specified plane is included in the first new cuboid, not the second.
        """
        cx, cy, cz = cuboid     # Don't really need another set, but it's a little easier to read.
        assert [x, y, z].count(None) == 2, f"Inputs (x, y, x) were {x}, {y}, {z}"
        nx1, ny1, nz1 = cuboid
        nx2, ny2, nz2 = cuboid
        if x is not None:
            nx1, nx2 = (cx[0], x), (x+1, cx[1])
        if y is not None:
            ny1, ny2 = (cy[0], y), (y+1, cy[1])
        if z is not None:
            nz1, nz2 = (cz[0], z), (z+1, cz[1])

        return (nx1, ny1, nz1), (nx2, ny2, nz2)

    def split_cuboid(top_cub, layer):
        """
        Split top cuboid into two, split along a boundary with layer. Return the two halves.

        :param top_cub: The layer to split, cuboid only.
        :param layer: The layer below top, cuboid only.
        :return: The two cuboids made from top.  Does not return the command.
        """
        # Figure out where to split it.
        tx, ty, tz = top_cub
        lx, ly, lz = layer

        if tx[0] != lx[0]:
            return split_at(top_cub, x=lx[0]-1)
        if tx[1] != lx[1]:
            return split_at(top_cub, x=lx[1])
        if ty[0] != ly[0]:
            return split_at(top_cub, y=ly[0]-1)
        if ty[1] != ly[1]:
            return split_at(top_cub, y=ly[1])
        if tz[0] != lz[0]:
            return split_at(top_cub, z=lz[0]-1)
        if tz[1] != lz[1]:
            return split_at(top_cub, z=lz[1])
        raise AssertionError("Something should have matched!")

    def get_change(top, lowers):
        """
        Return the count of cubes turned on by the top layer (may be negative).

        :param top: The top layer for which to return the change count.  top[0] must be True (on) or False (off).
        :param lowers: All previously applied layers, with layer[0] being the newest.
        :return: The count of cubes which were turned on by top.
        """

        # Shrink all instructions to size of this one.
        lowers = shrink(top, lowers)

        if not lowers:
            # At the bottom.  Assume that all cubes are off.
            if top[0]:
                return get_size(top[1])
            return 0

        next_layer = lowers[0]
        # If the next lower is full size, then we don't need to go any lower.
        if next_layer[1] == top[1]:
            # If that layer is the same as this, then nothing has changed.
            if next_layer[0] == top[0]:
                return 0
            size = get_size(top[1])
            return size if top[0] else -size

        # We aren't at the bottom and the next layer down doesn't cover everything.
        # Split this top into two chunks and try again on each of those.
        change = 0
        for chunk in split_cuboid(top[1], next_layer[1]):
            chunk = (top[0], chunk)
            change += get_change(chunk, lowers)
        return change

    # Done defining functions. Read the input data.
    instructions = []
    lines = read_data('day22.data')
    for line in lines:
        turn, line = line.split(' ', 1)
        turn = True if turn == 'on' else False
        x, y, z = line.split(',')
        x = x[2:].split('..')
        y = y[2:].split('..')
        z = z[2:].split('..')
        x = tuple([int(x) for x in x])
        y = tuple([int(x) for x in y])
        z = tuple([int(x) for x in z])
        tmp = (bool(turn), (x, y, z))
        instructions.append(tmp)

    if max_size is not None:
        # Shrink everything down in size for part one.
        instructions = shrink((None, ((-max_size, max_size),)*3), tuple(instructions), all=True)

    # Walk through the steps, counting how many cubes each one turned on.
    on = 0
    layers = []     # Newest layer is [0].
    for instruction in instructions:
        debug(f"Doing step", instruction)
        delta = get_change(instruction, tuple(layers))
        layers = [instruction] + layers
        on += delta
        debug(f"... which gave a delta of {delta} for a total of {on} cubes on.")

    print(f"Answer for day 22 part {part}: {on}")


def main():
    part2(max_size=50, part=1)
    part2()
