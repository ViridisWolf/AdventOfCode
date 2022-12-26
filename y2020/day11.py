#!/usr/bin/env python


from AdventOfCode import read_data


class GameOfLife:
    # The seating logic is basically Conway's Game of Life, but with slightly different rules.
    _floor = '.'
    _empty = 'L'
    _occupied = '#'

    def __init__(self, floor_plan, too_crowded=4, sight=False):
        self.board = {}
        self._width = 0
        self._height = 0
        self.iteration = 0
        self.too_crowded = too_crowded
        self.sight = sight

        self._height = len(floor_plan)
        self._width = len(floor_plan[0])
        for y, row in enumerate(floor_plan):
            for x, cell in enumerate(row):
                self.board[(x, y)] = cell

    def get_neighbors(self, cell_loc):
        """ Return the number of living/occupied cells in the eight directions. """
        # print(f"Getting neighbor count for {cell_loc}")
        x, y = cell_loc
        count = 0
        for d2x, d2y in [(-1, -1), (0, -1), (1, -1),
                         (-1,  0),          (1,  0),
                         (-1,  1), (0,  1), (1,  1)]:
            dx, dy = d2x, d2y
            while (0 <= x + dx < self._width) and (0 <= y + dy < self._height):
                neigh = self.board[(x + dx, y + dy)]
                if neigh == self._occupied:
                    count += 1
                    if count == self.too_crowded:
                        return self.too_crowded
                    break
                elif neigh == self._empty or not self.sight:
                    # Can't see past an empty seat.
                    break
                dx += d2x
                dy += d2y

        return count

    def step(self):
        """ Do one iteration of the game logic. """
        # All changes between iterations happen simultaneously, so keep the new state separate until finished.
        next_board = self.board.copy()
        for cell_loc, cell in self.board.items():
            if cell == self._floor:
                continue

            neighbors = self.get_neighbors(cell_loc)
            if neighbors == 0:
                next_board[cell_loc] = self._occupied
            if neighbors >= self.too_crowded:
                next_board[cell_loc] = self._empty
        self.board = next_board
        self.iteration += 1
        # print(f"Iteration {self.iteration} board state:")
        # self.print_board()

    def run_to_end(self):
        """ Do iterations of the seating logic until the state stops changing. """
        while True:
            prev_state = self.board.copy()
            self.step()
            if self.board == prev_state:
                # Reached steady state.
                break

    def get_occupied_count(self):
        """ Return the count of occupied/living seats/cells. """
        return sum([c == self._occupied for c in self.board.values()])

    def print_board(self):
        """ Print the current board layout. """
        for y in range(self._height):
            row = ''
            for x in range(self._width):
                row += self.board[(x, y)]
            print(row)
        print()


def day(lines):
    seating = GameOfLife(lines)
    # print("Initial seating layout:")
    # seating.print_board()
    seating.run_to_end()
    # print("Final seating layout:")
    # seating.print_board()
    # print(f"Answer for 2020 day 11 part 1: {seating.get_occupied_count()}")
    answer1 = seating.get_occupied_count()

    seating = GameOfLife(lines, too_crowded=5, sight=True)
    # print("Initial seating layout:")
    # seating.print_board()
    seating.run_to_end()
    # print("Final seating layout:")
    # seating.print_board()
    # print(f"Answer for 2020 day 11 part 2: {seating.get_occupied_count()}")
    answer2 = seating.get_occupied_count()

    return answer1, answer2


def main():
    lines = read_data(__file__)
    return day(lines)


expected_answers = 2222, 2032
