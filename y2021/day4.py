#!/usr/bin/env python

from . import read_data


def day4():
    def get_columns(board):
        """ Return an iterable of the values in each column of the board. """
        columns = []
        for col in range(len(board[0])):
            columns.append([row[col] for row in board])
        return columns

    def has_won(board, drawn):
        """ Return True if the board has won."""
        for row in board + get_columns(board):
            if all(map(lambda x: x in drawn, row)):
                return True

    # Read input.
    lines = read_data('day4.data')
    draws = [int(x) for x in lines[0].split(',')]
    boards = []
    board = None
    for line in lines[1:] + ['']:
        if not line:
            # Start a new board.
            if board is not None:
                boards.append(board)
            board = []
        else:
            row = [int(x) for x in line.split()]
            board.append(row)
    assert board == []

    # Play.
    drawn = []
    winners = []
    for draw in draws:
        drawn.append(draw)
        # Find the winners.
        for board in boards[:]:
            if has_won(board, drawn):
                # Bingo!
                winners.append([board, tuple(drawn)])
                boards.remove(board)
        if not boards:
            break

    # Scoring.
    for part, (board, drawn) in enumerate(winners[0:1] + winners[-1:], start=1):
        assert len([x for row in board for x in row]) == len(set([x for row in board for x in row])), "Boards must not repeat numbers."
        unmarked_sum = sum(set([x for row in board for x in row]).difference(drawn))
        score = unmarked_sum * drawn[-1]
        print(f"Answer for 2021 day 4 part {part}: {score}")
        assert score == (58374 if part == 1 else 11377), f"Calculated score was {score} for part {part}."


def main():
    day4()
