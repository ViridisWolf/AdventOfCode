#!/usr/bin/env python

from AdventOfCode import read_data


class PlanckRope:
    def __init__(self, tail_knots):
        self.visited_part1 = set([(0, 0)])
        self.visited_part2 = set([(0, 0)])
        self.head = (0, 0)
        self.tail = [(0, 0)] * tail_knots

    @staticmethod
    def move_knot(head, tail):
        """Returns the new location of the tail knot after moving it to follow the head knot. """
        dx = head[0] - tail[0]
        dy = head[1] - tail[1]

        if tail == head:
            pass
        elif (abs(dx) + abs(dy)) == 1 or (abs(dx) == 1 and abs(dy) == 1):
            # Touching; don't move.
            pass
        else:
            assert abs(dx) == 2 or abs(dy) == 2
            assert abs(dx) < 3 and abs(dy) < 3
            # For both x and y, take at most one step towards the head.
            x = tail[0] + (1 if dx > 0 else -1 if dx < 0 else 0)
            y = tail[1] + (1 if dy > 0 else -1 if dy < 0 else 0)
            tail = x, y
        return tail

    def move_head(self, dx, dy):
        """ Move head position, and then move all tail knots as needed. """
        self.head = self.head[0] + dx, self.head[1] + dy

        # Move all tail knots.
        head = self.head
        for index, knot in enumerate(self.tail):
            new_loc = self.move_knot(head, knot)
            self.tail[index] = new_loc
            head = new_loc

        # Update where the tail has been.
        self.visited_part1.add(self.tail[0])
        self.visited_part2.add(self.tail[-1])


def day9(data):
    rope = PlanckRope(tail_knots=9)
    for line in data:
        direction, amount = line.split(' ')
        amount = int(amount)
        for _ in range(amount):
            if direction == 'R':
                rope.move_head(1, 0)
            elif direction == 'L':
                rope.move_head(-1, 0)
            elif direction == 'U':
                rope.move_head(0, 1)
            elif direction == 'D':
                rope.move_head(0, -1)
            else:
                raise AssertionError

    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {len(rope.visited_part1)}")
    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {len(rope.visited_part2)}")
    return len(rope.visited_part1), len(rope.visited_part2)


def main():
    data = read_data()
    return day9(data)


expected_answers = 5902, 2445
