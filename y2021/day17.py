#!/usr/bin/env python

import math

from AdventOfCode import read_data


def day17():
    class Probe:
        def __init__(self, vel_x, vel_y):
            self.velocity_x = vel_x
            self.velocity_y = vel_y
            self.position_x = 0
            self.position_y = 0
            self.max_height = self.position_y

        def step_position(self):
            """ Step the probe's position forward in time once. """
            self.position_x += self.velocity_x
            self.position_y += self.velocity_y
            self.max_height = max(self.max_height, self.position_y)

            if self.velocity_x >= 1:
                self.velocity_x -= 1
            elif self.velocity_x <= -1:
                self.velocity_x += 1
            self.velocity_y -= 1

        def hit_target(self, target):
            """
            Returns True if the probe is within the target.  If the target _may_ hit the target in the future, returns
            None.  If the probe has passed the target, return the which direction was too far.
             """
            hit = True
            if self.position_x < target['x']['min']:
                if self.velocity_x == 0:
                    hit = 'y'
                else:
                    hit = None
            if self.position_y > target['y']['max']:
                hit = None
            if self.position_x > target['x']['max']:
                hit = 'x'
            if self.position_y < target['y']['min']:
                hit = 'y'
            return hit

    lines = read_data(__file__)
    for line in lines:
        if 'target area: ' in line:
            x, y = line[13:].split(', ')
            assert x.startswith('x=') and y.startswith('y=')
            x_min, x_max = (x[2:].split('..'))
            y_min, y_max = (y[2:].split('..'))
            target = {'x': {'min': int(x_min), 'max': int(x_max)},
                      'y': {'min': int(y_min), 'max': int(y_max)}}
            assert target['x']['min'] >= 0, "This function only supports the target being to the right."

    # Calculate the possible ranges.  These assume that the target will always be to the right and down.
    x_min = math.ceil((2*target['x']['min'] + 0.25)**0.5 - 0.5)
    x_max = target['x']['max']
    y_min = target['y']['min']
    y_max = abs(target['y']['min'])

    # Start trying starting conditions.
    hits = []
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            probe = Probe(x, y)
            while (hit := probe.hit_target(target)) is None:
                probe.step_position()
            if hit is True:
                hits.append((x, y, probe.max_height))
            elif hit == 'x':
                # Passed target horizontally before getting down to the target, so increasing vel_y more won't help.
                break

    highest = max([x[2] for x in hits])
    # print(f"Answer for 2021 day 17 part 1:", highest)
    # print(f"Answer for 2021 day 17 part 2:", len(hits))
    return highest, len(hits)


def main():
    return day17()


expected_answers = 13041, 1031
