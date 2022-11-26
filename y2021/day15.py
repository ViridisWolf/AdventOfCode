#!/usr/bin/env python

from collections import namedtuple

from . import read_data


def day15(tile_right, tile_down, part):
    Node = namedtuple("Node", 'x y')

    def repeat_map(risk_map, right, down):
        """ Add 1 to each risk value, update the nodes, return the map. """
        new_map = {}
        for node in risk_map:
            new_node = Node(node.x + right*map_width, node.y + down*map_height)
            risk = (risk_map[node] + right + down) - 1
            risk = (risk % 9) + 1
            new_map[new_node] = risk
        return new_map

    def neighbors(node):
        """ Returns the neighbor nodes. """
        neighs = []
        x, y = node.x, node.y
        if x + 1 < map_width:
            neighs.append(Node(x+1, y))
        if x - 1 >= 0:
            neighs.append(Node(x-1, y))
        if y + 1 < map_height:
            neighs.append(Node(x, y+1))
        if y - 1 >= 0:
            neighs.append(Node(x, y-1))
        return neighs

    def h_est(node, goal):
        """ Return an estimated risk from the node to the goal. """
        nodes_est = abs(goal.x - node.x) + abs(goal.y - node.y)
        risk_est = nodes_est * 5    # 5 is the average risk per node.
        return 1
        # return risk_est  # This causes incorrect results...

    lines = read_data('day15.data')
    map_width = len(lines[0])
    map_height = len(lines)

    risk_map = {}
    for row, line in enumerate(lines):
        for col, risk in enumerate(line):
            node = Node(int(col), int(row))
            risk_map[node] = int(risk)

    # Resize the map to the desired size.
    resized_map = {}
    for shift_right in range(tile_right):
        for shift_down in range(tile_down):
            resized_map.update(repeat_map(risk_map, shift_right, shift_down))
    # Update map stats.
    risk_map = resized_map
    map_height *= tile_right
    map_width *= tile_down
    start = Node(0, 0)
    goal = Node(map_width-1, map_height-1)

    # Start of A* search algorithm.
    came_from = {start: None}  # Dict of which node a was the previous on the best currently known path to the key node.
    visibles = set([start])    # Which nodes are visible and need to be scanned.
    cost_from_start = {}  # Value of each item is the so-far best found cost to that node from the start.
    cost_total_est = {} # Value of each item is the best estimated cost of a path through that node.
    cost_from_start[start] = 0  # Start has zero risk to get to start.
    cost_total_est[start] = h_est(start, goal)

    while visibles:
        current = min(visibles, key=lambda x: cost_total_est[x])
        if current == goal:
            # Found our way to the goal.
            break

        visibles.remove(current)
        for neigh in neighbors(current):
            relative_g = cost_from_start[current] + risk_map[neigh]
            if neigh not in cost_from_start or relative_g < cost_from_start[neigh]:
                # We found a better path to this node.  Update the stats.
                cost_from_start[neigh] = relative_g
                cost_total_est[neigh] = relative_g + h_est(neigh, goal)
                came_from[neigh] = current
                # Add it to the list of nodes to be scanned.
                visibles.add(neigh)
                # print(f'{current} neigh: {neigh}, g: {cost_from_start[neigh]}, f: {cost_total_est[neigh]}, h: {h_est(neigh, goal)}')

    # We must have found the path.
    assert current == goal
    path = [current]
    while came_from[current] is not None:
        prev = came_from[current]
        path = [prev] + path
        current = prev

    risk = sum([risk_map[n] for n in path[1:]])
    # Don't include risk of first node because there is no risk in leaving a node.
    print(f"Answer for 2021 day 15 part {part}: {risk}")  # 388, 2819
    # risk_path = [str(risk_map[x]) for x in path]; print(''.join(risk_path))


def main():
    day15(1, 1, 1)
    day15(5, 5, 2)
