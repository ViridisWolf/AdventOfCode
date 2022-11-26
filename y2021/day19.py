#!/usr/bin/env python

import copy
from functools import cache

from . import read_data

DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


class Scanner:
    def __init__(self, id, points=None):
        self.id = id
        self.points = set(points) if points else set()
        # is_absolute indicates the coordinates of the points are relative to itself or in the absolute reference frame.
        self.is_absolute = False
        self.position = None
        self.already_compared = set()

    def add_point(self, point):
        assert len(point) == 3
        self.points.add(tuple(point))


def get_translation(points, point1, point2):
    """
    Translate the beacon locations such that point1 from this scanner is at the same location as point2.
    :param points: The beacon location points.
    :param point1: A point/beacon location in this scanner.
    :param point2: The point location to translate point1 to.
    :return: Set of new beacon points, and the distance that the 'points' has been moved.
    """
    # Future: Check if this translation delta has already been done before for this 'points' set.
    assert point1 in points
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dz = point2[2] - point1[2]
    new_points = [(x + dx, y + dy, z + dz) for p in points for x, y, z in [p]]
    assert point2 in new_points
    return set(new_points), (dx, dy, dz)


def transform_90(points, axis):
    """ Rotate the points by 90 deg around the specified axis (x, y, or z). """
    assert axis in ['x', 'y', 'z']
    if axis == 'z':
        result = [(y, -x, z) for p in points for x, y, z in [p]]
    elif axis == 'y':
        result = [(z, y, -x) for p in points for x, y, z in [p]]
    elif axis == 'x':
        result = [(x, z, -y) for p in points for x, y, z in [p]]
    assert len(set(result)) == len(points)
    return tuple(result)


@cache
def _get_rotations(points):
    """ Return all 24 possible rotations of the scanner data. """
    # Rotate on the xy plane and on the xz plane.
    points = copy.deepcopy(points)
    rotated = set()
    # Use a set so that duplicate outputs don't get returned.

    rotated.add(points)
    for axis in 'xxxzyyyzxxxzyyyxzzzxxzzz':
        # One extra rotation near the end to get to the other side.
        # The duplicate copy will be removed since 'rotated' is a set.
        points = transform_90(points, axis)
        rotated.add(points)

    return rotated


def get_rotations(points):
    """ Wrapper around _get_rotations() so that I don't have to care about @cache and non-hashable inputs. """
    if type(points) in [list, set]:
        points = tuple(points)
    return _get_rotations(points)


def match_and_update(scanner, absolute_scanners, required_points=12):
    """
    For the specified scanner, find a scanner in the absolute_scanners list which it shares at least 12 points with.
    Update scanner to use the absolute coordinates for its points.  Also set its own position.

    :param required_points: How many points are required for a match to be valid.
    :param scanner: The Scanner object to find a match for.
    :param absolute_scanners: The scanners to compare against 'scanner', must be in absolute coordinates.
    :return: Whether a match was found.
    """
    assert not scanner.is_absolute
    # print("Absolute:", sorted(absolute_scanners[0].points))
    for abs_scan in absolute_scanners:
        if abs_scan.id in scanner.already_compared:
            continue
        for rot in get_rotations(scanner.points):
            # Translate this beacon set to the coordinate system of the absolute scanner.  Then, see if there are
            # at least 12 matching points.
            for rel_point in rot:
                for abs_point in abs_scan.points:
                    # Shift (translate) all of the points over such that this point from scanner is at the same
                    # coordinate as abs_point.  Check to see if enough other points match.
                    rot_abs, delta = get_translation(rot, rel_point, abs_point)
                    matches = len(set(rot_abs).intersection(abs_scan.points))
                    if matches >= required_points:
                        # Found a match!  Change the scanner's beacon points to use the absolute coordinates.
                        # print("Original points for this scanner:  ", scanner.points)
                        # print("Scanner points in current rotation:", rot_abs)
                        # print("Scanner0 points:                   ", abs_scan.points)
                        # print("Intersecting points:               ", set(rot_abs).intersection(abs_scan.points))
                        scanner.points = set(rot_abs)
                        scanner.is_absolute = True
                        scanner.position = delta
                        debug(f"Absolute coordinates found for scanner {scanner.id} with {matches} matches")
                        return True
        scanner.already_compared.add(abs_scan.id)
    return False


def manhattan_distance(s1, s2):
    """ Return the sum of the distances between points in each axis. """
    s = 0
    for a, b in zip(s1.position, s2.position):
        s += abs(a - b)
    return s


def main():
    if DEBUG:
        # Do some sanity checking.
        tests()

    # Parse the scanner data.
    scanners = []
    lines = read_data('day19.data')
    for line in lines:
        if '-- scanner ' in line:
            id = int(line[11:].split()[0])
            scanner = Scanner(id)
            scanners.append(scanner)
        if ',' in line:
            x, y, z = [int(n) for n in line.split(',')]
            scanner.add_point([x, y, z])

    # Set scanner 0 as the absolute point of reference.
    scanners[0].is_absolute = True
    scanners[0].position = (0, 0, 0)

    # For each scanner, compare it to all scanners which are already in absolute coordinates.
    relative_scanners = scanners[1:]
    abs_scanners = [scanners[0]]
    while relative_scanners:
        todo = len(relative_scanners)
        for rel_scan in relative_scanners[:]:
            found_match = match_and_update(rel_scan, abs_scanners)
            if found_match:
                # Add the newly matched scanner to the list of scanners which have absolute coordinates.
                abs_scanners.append(rel_scan)
                relative_scanners.remove(rel_scan)
                debug(f"Scanner {rel_scan.id} is at {rel_scan.position}.")
        #relative_scanners = [s for s in relative_scanners if not s.is_absolute]
        assert len(relative_scanners) < todo, "No match found in last pass!"

    # All scanners have been converted to absolute coordinates.  Now make the final map.
    beacon_maps = set()
    for scanner in scanners:
        for point in scanner.points:
            beacon_maps.add(point)
    print(f"Answer for 2021 day 19 part 1: {len(beacon_maps)}")

    dist = 0
    for index, s1 in enumerate(scanners):
        for s2 in scanners[index:]:
            dist = max(dist, manhattan_distance(s1, s2))
    print(f"Answer for 2021 day 19 part 2:", dist)


def tests():
    """ Use a few small examples to make sure that the rotation functions can provide some correct results. """
    p0 = [(-1, -1, 1), (-2, -2, 2), (-3, -3, 3), (-2, -3, 1), (5, 6, -4), (8, 0, 7)]
    ps = []
    ps.append({(1, -1, 1), (2, -2, 2), (3, -3, 3), (2, -1, 3), (-5, 4, -6), (-8, -7, 0)})
    ps.append({(-1, -1, -1), (-2, -2, -2), (-3, -3, -3), (-1, -3, -2), (4, 6, 5), (-7, 0, 8)})
    ps.append({(1, 1, -1), (2, 2, -2), (3, 3, -3), (1, 3, -2), (-4, -6, 5), (7, 0, 8)})
    ps.append({(1, 1, 1), (2, 2, 2), (3, 3, 3), (3, 1, 2), (-6, -4, -5), (0, 7, -8)})

    rotations = [set(x) for x in get_rotations(p0)]
    assert len(rotations) == 24
    for p in ps:
        assert p in rotations

    # Check translation and matching.
    s0 = Scanner(0, p0)
    s1 = s0
    assert match_and_update(s1, [s0], required_points=6)
    assert s1.position == (0, 0, 0)
    s1 = Scanner(1, {(-1+1, -1+5, 1-7), (-2+1, -2+5, 2-7), (-3+1, -3+5, 3-7), (-2+1, -3+5, 1-7), (5+1, 6+5, -4-7), (8+1, 0+5, 7-7)})
    assert match_and_update(s1, [s0], required_points=6)
    assert s1.position == (-1, -5, +7)
    s1 = Scanner(1, {(1, 1, 1), (2, 2, 2), (3, 3, 3), (3, 1, 2), (-6, -4, -5), (0, 7, -8)})
    assert match_and_update(s1, [s0], required_points=6)
    assert s1.position == (0, 0, 0)
