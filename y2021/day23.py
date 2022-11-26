#!/usr/bin/env python3

from functools import cache

DEBUG = False
A, B, C, D = 'A', 'B', 'C', 'D'


def debug(*args):
    if DEBUG:
        print(*args)


def print_steps(steps):
    """ Print the steps of the solution in a similar format to how the examples were done. """
    for step in steps:
        cost, hall, rooms = step
        hall = [x if x else '.' for x in hall]
        rooms = list(rooms)
        rooms = [[x if x else '.' for x in r] for r in rooms]

        if cost is not None:
            print(f"\nMoving at a cost of {cost} yields:")
        print('#'*13)
        print('#' + ''.join(hall) + '#')
        for i in range(len(rooms[0])):
            print(('  #' if i else '###') + '#'.join([x[i] for x in rooms]) + ('#  ' if i else '###'))
        print('  #########  ')


def day23(part=2):
    move_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    desired_room = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    all_rooms = [('r', x, y) for x in range(4) for y in range(4)]
    all_valid_halls = [('h', x) for x in [0, 1, 3, 5, 7, 9, 10]]
    all_valid_locations = all_valid_halls + all_rooms

    @cache
    def path_distance(starting, ending, hall, rooms):
        """ Returns the count of moves to ending if the intermediates are empty, else None.  Assumes end is empty."""
        distance = 1    # The 1 is the ending point.
        in_hall = starting[0] == 'h'    # Record if the amph is already in the hall and thus taking a space.

        # Because this function assumes the end is empty, then the movement is symmetric.  Always do the calculation
        # as if starting in the hall.
        if starting[0] == 'r':
            starting, ending = ending, starting

        assert starting[0] == 'h'
        r, b = ending[1:]
        if b > 0:
            # Check that the between beds are empty.
            if any(x is not None for x in rooms[r][0:b]):
                debug(f"Path is blocked at {('r', r, 0)}")
                return
        distance += len(rooms[r][0:b])
        # The room is clear.  Now check that the hall is clear between the room and starting.
        h_end = 2 + (r*2)
        h_start = starting[1]
        h_start, h_end = min(h_start, h_end), max(h_start, h_end)
        if hall[h_start: h_end+1].count(None) < (len(hall[h_start: h_end+1]) - (1 if in_hall else 0)):
            debug(f"Path is blocked at hall {h_start}:{h_end}: {hall[h_start:h_end]}")
            # Blocked.
            return
        # The path is clear!
        distance += h_end - h_start     # No abs() needed because these are already sorted.
        return distance

    @cache
    def is_done(rooms):
        """ Return True if the rooms have the correct amphs in them, else False """
        size = len(rooms[0])
        if rooms[0].count('A') == size:
            if rooms[1].count('B') == size:
                if rooms[2].count('C') == size:
                    if rooms[3].count('D') == size:
                        return True
        return False

    @cache
    def get_shortest_cost(hall, rooms, cost, best_cost=None):
        """
        Find the lowest cost path by recursively trying every possibility.

        :param hall: The hall tuple indicating where amphs are.
        :param rooms: The rooms tuple of tuple showing where amphs are.
        :param cost: The cost to reach the current state.
        :param best_cost: The cost of the best known path.
        :return: (best cost, steps)
        """

        # Store the room state, cost, and such.
        steps = ()    # [(cost, new_hall, new_rooms)]

        # Check to see if we should stop.
        if is_done(rooms):
            return cost, ()
        if best_cost and cost >= best_cost:
            return None, ()

        # Look for moves from all possible locations.
        for location in all_valid_locations:
            if 'h' == location[0]:
                # Find an amph that can move.
                if not hall[location[1]]:
                    continue
                amph = hall[location[1]]
                # Amph is in hallway
                debug(f"There is an {amph} amph at {location}.  Hall: {hall}")
                # Move it to all possible room locations.
                for dest in all_rooms:
                    r, b = dest[1:]
                    if r != desired_room[amph]:
                        # Don't want to move to that room.
                        continue
                    if rooms[r][b] is not None:
                        # Destination is not empty.
                        continue
                    if not all(x == amph for x in rooms[r][b+1:]):
                        # Can't move into a bed if the further beds are not filled with the correct amph type.
                        continue
                    debug(f"Amph {amph} at {location} wants to move to {dest}")
                    # We found a good bed!  Now see if we can get there.
                    dist = path_distance(location, dest, hall, rooms)
                    if dist is None:
                        # Breaking since there will only ever be one valid bed destination.
                        debug(f"Path from {location} to {dest} is blocked.")
                        break
                    # We can move!  Do the move and update the state for the next iteration.
                    new_cost = cost + (move_costs[amph] * dist)
                    new_hall, new_room = list(hall), list(rooms[r])
                    new_hall[location[1]] = None
                    new_room[b] = amph
                    new_rooms = rooms[:r] + (tuple(new_room),) + rooms[r+1:]
                    debug(f"New state after {amph} at {location} moves to {dest} - halls: {new_hall}, rooms: {new_rooms}")
                    possible_best, more_steps = get_shortest_cost(tuple(new_hall), new_rooms, new_cost, best_cost=best_cost)
                    debug(f"If amph {amph} at {location} moves to {dest} at a cost of {new_cost-cost}, then the best cost after that is {possible_best}.")
                    if best_cost is not None and (possible_best is None or possible_best >= best_cost):
                        continue
                    # Found a good path.
                    best_cost = possible_best
                    steps = ((new_cost-cost, new_hall, new_rooms),) + more_steps

            elif location[0] == 'r':
                r, b = location[1:]
                # Find an amph.
                amph = rooms[r][b]
                if amph is None:
                    continue
                # Check if this amph is at its final place.
                if r == desired_room[amph]:
                    if all(x == amph for x in rooms[r][b:]):
                        # This amph and all others deeper in the room are at their final spots.
                        continue

                # We found an amph that wants to move.  Now check for all possible destinations.
                if cost == 0:
                    debug(f"Checking if amph {amph} at {location} can move.")
                for dest in all_valid_halls:
                    if hall[dest[1]]:
                        if cost == 0:
                            debug(f"Can't move to {dest} because it is not empty.")
                        continue
                    dist = path_distance(location, dest, hall, rooms)
                    if dist is None:
                        if cost == 0:
                            debug(f"Can't move to {dest} because the path is blocked.")
                        continue
                    if cost == 0:
                        debug(f"Can move to {dest}.")
                    # We can move to the hall!  Do the move and update the state for the next iteration.
                    new_cost = cost + (move_costs[amph] * dist)
                    new_hall, new_room = list(hall), list(rooms[r])
                    new_hall[dest[1]] = amph
                    new_hall = tuple(new_hall)
                    new_room[b] = None
                    new_rooms = rooms[:r] + (tuple(new_room),) + rooms[r+1:]
                    assert len(new_rooms) == 4, f"Invalid 'new_rooms': {new_rooms}"
                    possible_best, more_steps = get_shortest_cost(tuple(new_hall), new_rooms, new_cost, best_cost=best_cost)
                    if cost==0:
                        debug(f"Best solution cost after amph {amph} at {location} moves to {dest}: {possible_best}")
                    if best_cost is not None and (possible_best is None or possible_best >= best_cost):
                        continue
                    # Found a good path.
                    best_cost = possible_best
                    steps = ((new_cost-cost, new_hall, new_rooms),) + more_steps
            else:
                raise AssertionError()

        # We've iterated through every possible move, recursively.
        return best_cost, steps

    ################################################
    # Puzzle input:
    #    #############
    #    #...........#
    #    ###C#B#D#A###
    #      #B#D#A#C#
    #      #########
    # After part 2 adjustment:
    #    #############
    #    #...........#
    #    ###C#B#D#A###
    #      #D#C#B#A#
    #      #D#B#A#C#
    #      #B#D#A#C#
    #      #########

    # Index zero of each room is the spot near the hall.  Room #0 is the left most.
    if part == 1:
        all_rooms = [('r', x, y) for x in range(4) for y in range(2)]
        all_valid_locations = all_valid_halls + all_rooms
        hall = tuple([None] * 11)
        rooms = ((C, B),
                 (B, D),
                 (D, A),
                 (A, C))
    elif part == 2:
        hall = tuple([None] * 11)
        rooms = ((C, D, D, B),
                 (B, C, B, D),
                 (D, B, A, A),
                 (A, A, C, C))
    elif part == 'test':
        hall = (A, A, None, D, None, None, None, None, None, A, D)
        rooms = ((None, None, None, A),
                 (B, B, B, B),
                 (C, C, C, C),
                 (None, None, D, D),)

    # Done setting up, now find the solution.
    lowest_cost, steps = get_shortest_cost(hall, rooms, 0, None)
    if DEBUG:
        print_steps(((None, hall, rooms),) + steps)
    print(f"Answer for 2021 day 23 part {part}: {lowest_cost}")


def main():
    day23(part=1)
    day23()
