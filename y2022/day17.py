#!/usr/bin/env python

from AdventOfCode import read_data

WALL_LEFT = 0
WALL_RIGHT = 8


def collision(piece, board, dx, dy):
    """
    Return true if there would be a collision in that direction.

    :param piece: Dict of piece elements.
    :param board: Set of static points.
    :param dx: Movement right.
    :param dy: Movement down.
    :return: If there would be a collision.
    """

    shifted = offset_piece(piece, dx, dy)

    # Check if hitting wall.
    shifted.sort()
    if shifted[0][0] <= WALL_LEFT or shifted[-1][0] >= WALL_RIGHT:
        return True
    # Check if hitting static pieces.
    if board.intersection(set(shifted)):
        return True
    # Check if hitting the floor.
    if min([y for (x, y) in shifted]) <= 0:
        return True

    return False


def offset_piece(piece, dx, dy):
    """ Return the piece list with shifted by the offset. """
    return [(x+dx, y+dy) for (x, y) in piece]


def print_board(board, highest):
    """ Display the tetris board. """
    print()
    for y in range(highest, 0, -1):
        row = [p for p in board if p[1] == y]
        line = f'|       |'
        for x, _ in row:
            line = line[:x] + '#' + line[x+1:]
        print(line)
    print('+-------+')


def day(line):
    """
    Do some tetris like movement of falling rocks into a chamber.

    Return how high the tetris rocks will be after 2022 rocks fall and after 1 trillion rocks fall.
    """

    # +x is right, +y is up.
    # Each shape has its lowest element on y=0 and leftest on x=0.
    shapes = [[(0, 0), (1, 0), (2, 0), (3, 0)],  # Horizontal line piece.
              [(1, 2), (0, 1), (1, 1), (2, 1), (1, 0)],  # Plus sign.
              [(2, 2), (2, 1), (0, 0), (1, 0), (2, 0)],  # Backwards L.
              [(0, 3), (0, 2), (0, 1), (0, 0)],  # Vertical line piece.
              [(0, 1), (1, 1), (0, 0), (1, 0)],  # Square piece.
              ]

    wind = [1 if w == '>' else -1 for w in line]
    rock_falls = 1_000_000_000_000

    # Methodology: Simulate the rocks falling and keep track of the rocks in a set.  Use set unions
    #              to check for collisions and x/y bounds checking collisions with the walls and
    #              floor.
    #
    #              There the tetris shapes repeat in a small loop, and the movement directions
    #              repeat in a larger loop.  Because there is nothing else going on, there should
    #              a repeating pattern that we can find.  It will likely take some time for the
    #              rock falls to stabilize into a pattern.
    #
    #              So, while doing that simulation, save rate of change in the final output (the
    #              height) in a list.  Then look for repeating patterns in that rate with runs long
    #              enough to have confidence that seeing a repetition of the pattern is not random
    #              chance.  The search can then be stopped and the pattern used to quickly get the
    #              answer for any higher number of rock falls.
    #

    board = set()
    highest = 0
    windex = 0
    prev_height = 0
    delta_height = []
    pattern = None
    for index in range(rock_falls):
        # Spawn a piece.
        shape = shapes[index % len(shapes)]
        # Offsets need to be +1 compared to AoC numbers because 0 is wall/floor.
        shape = offset_piece(shape, +3, highest + 4)

        moving = True
        while moving:
            # Check for side collision.
            dx = wind[windex % len(wind)]
            windex += 1
            if not collision(shape, board, dx, 0):
                shape = offset_piece(shape, dx, 0)

            # Check for downward collision.
            if collision(shape, board, 0, -1):
                # Add to board if downward collision.
                board.update(shape)
                highest = max([highest] + [y for (x, y) in shape])
                moving = False
            else:
                # Move the piece down into the empty space.
                shape = offset_piece(shape, 0, -1)

        delta_height.append(highest - prev_height)
        prev_height = highest

        if index == 2021:
            # Save off the answer for part 1.
            answer1 = highest

        # Look for a repeating pattern.
        if len(delta_height) < 10000:
            # The above 10_000 value was chosen for speed and found by experimentation.
            # It should be higher than the unstable region plus a few repetitions of the pattern.
            continue
        for back in range(len(shapes)*10, len(delta_height)//3, len(shapes)):
            # There are 5 shapes, so there must be a repeating pattern with a multiple of that length.
            pattern = delta_height[-back:]
            for offset in range(2, 4):
                # Look for at least 2(?) additional copies of the pattern.
                if not delta_height[-back*offset:-back*(offset-1)] == pattern:
                    pattern = None
                    break
            if pattern:
                prepattern_index = index + 1
                prepattern_sum = highest
                # print(f"prepattern_index: {prepattern_index}, prepattern_sum: {prepattern_sum}, pattern length: {len(pattern)}")
                break
        if pattern:
            break

    # Final part 2 calculations.
    height = 0
    # Subtract off the rock fallen from before the pattern started.
    height += prepattern_sum
    rock_falls -= prepattern_index
    # The rest of the rock_falls repeat.
    height += (rock_falls // len(pattern)) * sum(pattern)
    rock_falls = rock_falls % len(pattern)
    height += sum(pattern[:rock_falls])
    answer2 = height

    return answer1, answer2


def main():
    data = read_data()
    line = data[0]
    return day(line)


expected_answers = 3232, 1585632183915
