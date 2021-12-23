#!/usr/bin/env python3
from functools import cache

from .days import read_data


DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)

# Idea:
#   - For each amphipod and each possible move for that amphipod, try that move and recurse.
#   - Keep track of the best found solution so far, and end as soon as current cost exeeds that.
#   - Must allow returning inf cost (i.e. no solution).
#   - How to code up the map?

def part1():
    move_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    desired_room = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

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
        if b == 1:
            # Check that the between bed is empty.
            if rooms[r][0] is not None:
                debug(f"Path is blocked at {('r', r, 0)}")
                return
            distance += 1
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
        if rooms[0].count('A') == 2:
            if rooms[1].count('B') == 2:
                if rooms[2].count('C') == 2:
                    if rooms[3].count('D') == 2:
                        return True
        return False


    ################################################
    lines = read_data('day23_test.data')
    for line in lines:
        if '.' in line:
            hall = [None]*(line.count('.'))

    hall = tuple([None] * 11)

    # Index zero of each room is the spot near the hall.  Room #0 is the left most.
    # Real input.
    rooms = (('C', 'B'),
             ('B', 'D'),
             ('D', 'A'),
             ('A', 'C'))
    # Test input.
    hall_test = (None,None,None,None,None,'D',None,None,None,None,None)
    rooms_test = ((None, 'A'),
                  ('B', 'B'),
                  ('C', 'C'),
                  ('D', 'A'),)
    #hall = (None,None,None,None,None,None,None,None,None,'A',None)
    #rooms_test = ((None, 'A'),
    #              ('B', 'B'),
    #              ('C', 'C'),
    #              ('D', 'D'),)
    #rooms = rooms_test
    #hall = hall_test

    @cache
    def get_shortest_cost(hall, rooms, cost, best_cost=None):
        """

        :param hall:
        :param rooms:
        :param cost: The cost to reach the current state.
        :param best_cost: The cost of the best known path.
        :return:
        """

        # Check to see if we should stop.
        if is_done(rooms):
            return cost
        if best_cost and cost >= best_cost:
            return None

        all_rooms = [('r', x, y) for x in range(4) for y in range(2)]
        all_valid_halls = [('h', x) for x in [0,1,3,5,7,9,10]]
        all_locations = all_valid_halls + all_rooms

        # Look for moves from all possible locations.
        for location in all_locations:
            if 'h' == location[0]:
                # Find an amph that can move.
                if not hall[location[1]]:
                    continue
                amph = hall[location[1]]
                # Amph is in hallway
                debug(f"There is an {amph} amph at {location}")
                # Move it to all possible room locations.
                for bed in all_rooms:
                    r, b = bed[1:]
                    if r != desired_room[amph]:
                        continue
                    if rooms[r][b] is not None:
                        continue
                    if b == 0 and rooms[r][1] != amph:
                        # Can't move into the bed 0 if a different amph type is still in the last bed.
                        continue
                    debug(f"Amph {amph} at {location} wants to move to {bed}")
                    # We found a good bed!  Now see if we can get there.
                    dist = path_distance(location, bed, hall, rooms)
                    if dist is None:
                        # Breaking since there will only ever be one valid bed destination.
                        debug(f"Path from {location} to {bed} is blocked.")
                        break
                    # We can move!  Do the move and update the state for the next iteration.
                    new_cost = cost + (move_costs[amph] * dist)
                    new_hall, new_room = list(hall), list(rooms[r])
                    new_hall[location[1]] = None
                    new_room[b] = amph
                    new_rooms = rooms[:r] + (tuple(new_room),) + rooms[r+1:]
                    debug(f"New state after {amph} at {location} moves to {bed} - halls: {new_hall}, rooms: {new_rooms}")
                    possible_best = get_shortest_cost(tuple(new_hall), new_rooms, new_cost, best_cost=best_cost)
                    debug(f"If amph {amph} at {location} moves to {bed}, then the best cost after that is {possible_best}.")
                    if best_cost is not None and (possible_best is None or possible_best >= best_cost):
                        continue
                    # Found a good path.
                    best_cost = possible_best

            elif location[0] == 'r':
                r, b = location[1:]
                # Find an amph.
                amph = rooms[r][b]
                if amph is None:
                    continue
                # Check if this amph is at its final place.
                if r == desired_room[amph]:
                    if b == 1:
                        continue
                    if b == 0 and rooms[r][1] == amph:
                        continue

                # We found an amph that wants to move.  Now check for all possible destinations.
                if cost==0:
                    debug(f"Checking if amph {amph} at {location} can move.")
                for h in all_valid_halls:
                    if hall[h[1]]:
                        if cost==0:
                            debug(f"Can't move to {h} because it is not empty.")
                        continue
                    dist = path_distance(location, h, hall, rooms)
                    if dist is None:
                        if cost==0:
                            debug(f"Can't move to {h} because the path is blocked.")
                        continue
                    if cost==0:
                        debug(f"Can move to {h}.")
                    # We can move to the hall!  Do the move and update the state for the next iteration.
                    new_cost = cost + (move_costs[amph] * dist)
                    new_hall, new_room = list(hall), list(rooms[r])
                    new_hall[h[1]] = amph
                    new_room[b] = None
                    new_rooms = rooms[:r] + (tuple(new_room),) + rooms[r+1:]
                    assert len(new_rooms) == 4, f"Invalid 'new_rooms': {new_rooms}"
                    possible_best = get_shortest_cost(tuple(new_hall), new_rooms, new_cost, best_cost=best_cost)
                    if cost==0:
                        debug(f"Best solution cost after amph {amph} at {location} moves to {h}: {possible_best}")
                    if best_cost is not None and (possible_best is None or possible_best >= best_cost):
                        continue
                    # Found a good path.
                    best_cost = possible_best
            else:
                raise AssertionError()

        # We've iterated through every possible move, recursively.
        return best_cost

    lowest_cost = get_shortest_cost(hall, rooms, 0, None)
    print(lowest_cost)

    # Too low: 13518


def main():
    part1()
