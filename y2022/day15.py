#!/usr/bin/env python

from AdventOfCode import read_data


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def row_covered(row, sensors, beacons, part=1):
    """
    Calculate how many points in the row are covered by the sensors, and which one is empty.

    :param row: The row (y) to check.
    :param sensors: Dictionary of sensor objects.
    :param beacons: Set of beacon locations.
    :param part: 1 if part 1, 2 if part 2.
    :return: 3-tuple: Count of points which cannot be beacons, x coordinate of an empty point, number of rows to skip.
    """
    # Calc the intersection of the line with each scanner's range.
    # Make this into a list of min/max of each region.  Find the gap or overlap between intersections.

    covered_count = 0
    not_covered_x = None
    x_limit = 0, 4000000
    skip = x_limit[1]

    covered_regions = []
    for sensor in sensors.values():
        sx, sy = sensor['location']
        sy_min = sensor['min_y']
        sy_max = sensor['max_y']

        # print(sensor)
        if not (sy_min <= row <= sy_max):
            # print(f"Sensor {sensor['location']} does not cover row.")
            continue

        side_width = sensor['range'] - abs(row - sy)
        covered_regions.append([sx - side_width, sx + side_width])
        # print(f"Sensor {sensor['location']} insects {covered_regions[-1]} (sides: {side_width}, range: {sensor['range']})")
    covered_regions.sort()
    # print(covered_regions)
    # TODO: Split this function into different parts.
    # TODO: Improve the skip value.

    prev = None
    for x_min, x_max in covered_regions:
        if part == 2:
            # Part 2 checks.
            if x_max < x_limit[0]:
                continue
            if x_min > x_limit[1]:
                continue
            if x_min < x_limit[0]:
                x_min = x_limit[0]
            if x_max > x_limit[1]:
                x_max = x_limit[1]

        if prev is not None and x_max < prev:
            # Total overlap.  Skip this region.
            continue
        # print("Adding", x2_max - x2_min + 1)
        covered_count += x_max - x_min + 1
        if prev is None:
            pass
        elif prev >= x_min:
            # Subtract off any overlap.
            # print("Removing", prev - x2_min + 1, "overlap")
            skip = min(skip, prev - x_min)
            covered_count -= prev - x_min + 1
        elif prev == x_min - 2:
            # Gap of one.  This should be the missing point.
            not_covered_x = x_min - 1
            skip = 0
        else:
            skip = 0
        prev = x_max

    if part == 1:
        # Remove any beacons in the line, as we only want the points which can't have beacons.
        covered_count -= len([b for b in beacons if b[1] == row])
        # print("Removing count of overlapping beacons:", len([b for b in beacons if b[1] == row]))

    skip = min(skip, x_limit[0] - covered_regions[0][0])
    skip = min(skip, max(r[1] for r in covered_regions) - x_limit[1])
    skip = max(skip, 0)
    # The divide by 2 is because a region overlap may shrink at up to 2 units per row.
    skip = skip // 2

    return covered_count, not_covered_x, skip


def day(data):
    sensors = {}
    beacons = set()
    for line in data:
        sx, extra = line.removeprefix('Sensor at x=').split(', y=', 1)
        sy, extra = extra.split(': ', 1)
        bx, by = extra.removeprefix('closest beacon is at x=').split(', y=')
        sx, sy, bx, by = int(sx), int(sy), int(bx), int(by)
        s_range = manhattan_distance((sx, sy), (bx, by))
        # min_x = sx - s_range
        # max_x = sx + s_range
        min_y = sy - s_range
        max_y = sy + s_range
        # if min_x > max_x:
        #     min_x, max_x = max_x, min_x
        if min_y > max_y:
            min_y, max_y = max_y, min_y

        sensor = {'sensor': len(sensors),
                  'location': (sx, sy),
                  'beacon': (bx, by),
                  # 'min_x': min_x,
                  # 'max_x': max_x,
                  'min_y': min_y,
                  'max_y': max_y,
                  'range': s_range
                  }
        sensors[(sx, sy)] = sensor
        beacons.add((bx, by))

    # Part 1.
    y = 2000000
    answer1, _, _ = row_covered(y, sensors, beacons, part=1)

    # Part 2.
    row = 0
    while 0 <= row <= 4000000:
        _, not_covered_x, skip = row_covered(row, sensors, beacons, part=2)
        if not_covered_x is not None:
            # This must be the empty spot.
            answer2 = not_covered_x*4000000 + row
            break
        # print(f"After row {row}, skipping ahead by {skip}")
        row += 1 + skip
    else:
        raise AssertionError("Unable to find the answer!")

    return answer1, answer2


def main():
    data = read_data()
    return day(data)


expected_answers = 4919281, 12630143363767
