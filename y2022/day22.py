#!/usr/bin/env python

from AdventOfCode import read_data


class Board:
    wall = '#'
    open = '.'
    void = ' '

    def __init__(self, data, part=1):
        self.map = {}
        self.part = part
        self.x_limits = [None]
        self.y_limits = [None]
        self.location = None
        self.facing = 90

        # Construct the board.
        for y, line in enumerate(data, 1):
            for x, char in enumerate(line, 1):
                if char == ' ':
                    continue
                elif char in ['#', '.']:
                    # Update the limits.
                    if y >= len(self.x_limits):
                        self.x_limits.append([x, x])
                    else:
                        self.x_limits[y][1] = x
                    while len(self.y_limits) <= x:
                        self.y_limits.append(None)
                    if self.y_limits[x] is None:
                        self.y_limits[x] = [y, y]
                    else:
                        self.y_limits[x][1] = y
                    # print(f"Adding {x, y} ({char}) to the map")
                    # Update the map.
                    if char == '#':
                        self.map[x, y] = self.wall
                    else:
                        assert char == '.'
                        self.map[x, y] = self.open
                else:
                    raise AssertionError

        # Create side transform functions for part 2.
        # This is hard-coded for my puzzle input.
        side_len = 50
        self.point_to_side = {}
        self.point_to_side.update({(x, y): 1 for x in range( 51,  51 + side_len) for y in range(  1,   1 + side_len)})
        self.point_to_side.update({(x, y): 2 for x in range(101, 101 + side_len) for y in range(  1,   1 + side_len)})
        self.point_to_side.update({(x, y): 3 for x in range( 51,  51 + side_len) for y in range( 51,  51 + side_len)})
        self.point_to_side.update({(x, y): 4 for x in range(  1,   1 + side_len) for y in range(101, 101 + side_len)})
        self.point_to_side.update({(x, y): 5 for x in range( 51,  51 + side_len) for y in range(101, 101 + side_len)})
        self.point_to_side.update({(x, y): 6 for x in range(  1,   1 + side_len) for y in range(151, 151 + side_len)})
        self.transforms = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
        self.transforms[1][( 0, -1)] = lambda x, y: (1,              151 + (x -  51)),  90
        self.transforms[1][(-1,  0)] = lambda x, y: (1,              101 + (50 -  y)),  90
        self.transforms[2][( 0, -1)] = lambda x, y: (1 + (x - 101),              200),   0
        self.transforms[2][( 1,  0)] = lambda x, y: (100,            101 + (50- y)), 270
        self.transforms[2][( 0,  1)] = lambda x, y: (100,            51  + (x - 101)), 270
        self.transforms[3][(-1,  0)] = lambda x, y: (  1 + (y - 51), 101),             180
        self.transforms[3][( 1,  0)] = lambda x, y: (101 + (y - 51), 50),                0
        self.transforms[4][( 0, -1)] = lambda x, y: (51,             51  + (x - 1)),  90
        self.transforms[4][(-1,  0)] = lambda x, y: (51,             1   + (150 - y)),  90
        self.transforms[5][( 1,  0)] = lambda x, y: (150,            1   + (150 - y)),   270
        self.transforms[5][( 0,  1)] = lambda x, y: (50, 151 + (x - 51)), 270
        self.transforms[6][( -1, 0)] = lambda x, y: (51 + (y - 151), 1), 180
        self.transforms[6][( 1,  0)] = lambda x, y: (51 + (y - 151), 150), 0
        self.transforms[6][( 0,  1)] = lambda x, y: (101 + (x - 1), 1), 180

        # Find the starting point.  It will be the left-most open spot in the top row (y=1).
        for x in range(self.x_limits[1][0], self.x_limits[1][1]+1):
            if self.map[x, 1] is self.open:
                self.location = (x, 1)
                break

    def get_adjacent(self, point, direction):
        """ Return the map item, location, and facing of the proposed move. """
        facing = self.facing
        if point in self.map:
            return self.map[point], point, facing

        x, y = point
        dx, dy = direction
        if self.part == 1:
            if dx:
                if x < self.x_limits[y][0]:
                    x = self.x_limits[y][1]
                elif x > self.x_limits[y][1]:
                    x = self.x_limits[y][0]
            if dy:
                if y < self.y_limits[x][0]:
                    y = self.y_limits[x][1]
                elif y > self.y_limits[x][1]:
                    y = self.y_limits[x][0]
        else:
            print(f"Transform from {point} in direction {direction}")
            if point == (0, 105): breakpoint()
            side = self.point_to_side[point[0] - direction[0], point[1] - direction[1]]
            transform, facing = self.transforms[side][direction]
            x, y = transform(x + dx, y + dy)

        new_point = x, y
        return self.map[new_point], new_point, facing

    def try_move(self, direction):
        """ Check if there is a wall in the specified direction, and move there if not. """
        dx, dy = direction
        assert -1 <= dx <= 1
        assert -1 <= dy <= 1
        x = self.location[0] + dx
        y = self.location[1] + dy
        space, new_location, new_facing = self.get_adjacent((x, y), (dx, dy))
        if space is self.open:
            self.location = new_location
            self.facing = new_facing

    def rotate(self, degrees):
        """ Rotate the current facing by the specified number of degrees. """
        assert degrees % 360 in [0, 90, 180, 270]
        self.facing = (self.facing + degrees) % 360

    def try_forward(self, length):
        """ Move forward by the specified number of steps or until a wall it encountered. """
        for _ in range(length):
            if self.facing == 0:
                direction = 0, -1
            elif self.facing == 90:
                direction = 1, 0
            elif self.facing == 180:
                direction = 0, 1
            elif self.facing == 270:
                direction = -1, 0
            else:
                raise AssertionError

            location = self.location
            self.try_move(direction)
            # print(f"Old location: {location}, new location: {self.location}, new facing: {self.facing}")
            if location == self.location:
                break

    def get_score(self):
        """ Return the size score of the current location. """
        score = 1000 * self.location[1]
        score += 4 * self.location[0]
        facing = ((self.facing - 90)//90) % 4
        score += facing
        return score


def day(data, part=1):
    assert data[-2] == ""
    board = Board(data[:-2], part=part)
    # print(f"Starting location: {board.location}")

    line = data[-1]
    command = ''
    for index, char in enumerate(line):
        command = command + char
        if char.isnumeric() and index+1 < len(line) and line[index+1].isnumeric():
            # Wait until the whole number has been read.
            continue
        elif char.isnumeric():
            # Move forward.
            board.try_forward(int(command))
        else:
            assert command in ['L', 'R']
            if command == 'L':
                board.rotate(-90)
            else:
                board.rotate(90)
        print(f"After command {command}: facing {board.facing}, location {board.location}")
        command = ""

    return board.get_score()


def main():
    data = read_data(__file__)
    answer1 = day(data, part=1)
    answer2 = day(data, part=2)
    return answer1, answer2


expected_answers = 196134, 146011
