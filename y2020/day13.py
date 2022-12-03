#!/usr/bin/env python

import math

from AdventOfCode import read_data


def part1(data):
    best_wait = 999999
    best_bus = None

    min_depature = int(data[0])
    for period in data[1].split(','):
        if period == 'x':
            continue

        period = int(period)
        wait_time = period - (min_depature % period) % period
        if wait_time < best_wait:
            best_wait = wait_time
            best_bus = period
    # print(f"You: {min_depature}, best bus: {best_bus}, wait: {best_wait}")

    print(f"Answer for 2020 day 13 part 1: {best_bus * best_wait}")


def part2(data):
    # 1) Search timestamps until a match is found for just the first bus.
    #    We know that this first bus will be back in the same position again every period.
    # 2) Then, look for an answer for the second bus.  However, we know that the first bus will not be in the correct
    #    position unless we've jumped ahead by a multiple of the first bus's period.  So, only increase the timestamp by
    #    multiples of the first bus's period.
    # 3) Once we found a match for the second bus, we know that this pattern will repeat every time we jump ahead by the
    #    pattern's period.  The pattern's period is the least-common-multiple of all periods that were used to make the
    #    pattern (i.e. LCM of all periods of buses matched so far).
    # 4) Repeat #2, except jumping ahead by the LCM of the current pattern, until all buses have been matched.
    #
    # *) If the required wait time is greater than the bus's period, then add the minimum abnormal wait time (i.e. the
    #    time of the additional periods) as an offset (or subtract that abnormal time from the expected wait).

    lcm = 1
    timestamp = 0
    buses = []
    for pos, bus in enumerate(data[1].split(',')):
        if bus == 'x':
            continue
        period = int(bus)
        buses.append((pos, period))

    total_lcm = math.lcm(*[b[1] for b in buses])

    for pos, period in buses:
        equivalent_pos = pos - ((pos//period) * period)
        # print(f"Bus {period} needs wait time of {pos}, which requires it to wait {pos//period} additional periods.")

        while True:
            wait_time = ((period - (timestamp % period)) % period)
            if wait_time == equivalent_pos:
                lcm = math.lcm(lcm, period)
                # print(f"Found the match for {period} at {timestamp}+{pos}.")
                # print(f"New lcm: {lcm}")
                break
            timestamp += lcm
            if timestamp > total_lcm:
                # If we reach the LCM of all bus periods, then we've covered every possible pattern.  So, if we reached
                # here, then either we missed the solution or there is no solution.
                print(f"Failed!  Timestamp: {timestamp}")
                return

    print(f"Answer for 2020 day 13 part 2: {timestamp}")


def main():
    data = read_data(__file__)
    part1(data)
    part2(data)
