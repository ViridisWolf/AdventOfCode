#!/usr/bin/env python

import math
import multiprocessing
import re

from AdventOfCode import read_data

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"


class Blueprint:
    def __init__(self, bid, ore, clay, obsidian, geode, time_limit):
        self.id = bid
        self.cost = {
            ORE: tuple(ore),
            CLAY: tuple(clay),
            OBSIDIAN: tuple(obsidian),
            GEODE: tuple(geode)}
        self.resources = [0, 0, 0, 0]
        self.rates = [1, 0, 0, 0]
        self.time = 1
        self.time_limit = time_limit

        self.ideal = [max([clay[0], obsidian[0], geode[0]]),
                      max([ore[1], obsidian[1], geode[1]]),
                      max([ore[2], clay[2], geode[2]])]

    @staticmethod
    def produce_materials(duration, currents, rates):
        """ Add the amount of materials produced in the specified duration. """
        for material, amount in enumerate(currents):
            currents[material] += rates[material] * duration

    @staticmethod
    def remove_materials(amounts, currents):
        """ Remove the specified amounts of materials. """
        for material, amount in enumerate(amounts):
            currents[material] -= amount

    @staticmethod
    def time_until(required, current, rate):
        """ Return the number of turns until there are at least this amount of available materials. """
        min_time = 0
        for resource in range(3):
            if required[resource]:
                if not rate[resource]:
                    return None
                min_time = max(min_time, math.ceil((required[resource] - current[resource]) / rate[resource]))
        return min_time

    def print(self):
        print((f"id: {self.id}, "
               f"time: {self.time}, "
               f"resources: {self.resources}, "
               f"bots: {self.rates}"))


def get_optimum_geodes(blueprint):
    stack = [[blueprint.resources[:], blueprint.rates[:], blueprint.time,
              [(0, ORE), (1, CLAY), (2, OBSIDIAN), (3, GEODE)]]]
    best = 0
    while stack:
        resources, rates, timestamp, bot_types = stack.pop()
        if len(bot_types) > 1:
            stack.append([resources, rates, timestamp, bot_types[1:]])
        bot_num, bot_type = bot_types[0]

        bot_cost = blueprint.cost[bot_type]
        duration = blueprint.time_until(bot_cost, resources, rates)

        if duration is None:
            # Not producing the required materials, so will not be able to build this bot type.
            continue
        if bot_type != GEODE and rates[bot_num] >= blueprint.ideal[bot_num]:
            # We're already making as much as we need every turn, so skip building more bots.
            continue
        if bot_type != GEODE and rates[0] >= blueprint.cost[GEODE][0] and rates[2] >= blueprint.cost[GEODE][2]:
            # Generating enough ore and obsidian to make a geode bot every turn, so only make geode bots.
            continue

        # Add 1 to duration so that it includes the time to build the bot.
        duration += 1
        new_time = timestamp + duration
        new_resources = resources[:]
        new_rates = rates[:]
        if new_time <= blueprint.time_limit:
            # print(f"Minute {new_time-1}: Spend {bot_cost} to start building a {bot_type} bot.")
            blueprint.produce_materials(duration, new_resources, new_rates)
            blueprint.remove_materials(bot_cost, new_resources)
            new_rates[bot_num] += 1
            # print(f"Building {bot_type}, which will produce its first resource during turn {new_time}")

            # Add to stack for next turn.
            stack.append([new_resources, new_rates, new_time,
                          [(0, ORE), (1, CLAY), (2, OBSIDIAN), (3, GEODE)]])
        else:
            # No time to build the bot, so fast-forward to the end.
            duration = blueprint.time_limit + 1 - timestamp
            blueprint.produce_materials(duration, new_resources, new_rates)
            timestamp += duration
            best = max(best, new_resources[3])

    quality = blueprint.id * best
    # print(f"Completed blueprint {blueprint.id} in {iterations} iterations, with {best} geodes and {quality} quality.")
    return best, quality


def day(data, part):
    pattern = (r"Blueprint (\d+): "
               r"Each ore robot costs (\d+) ore. "
               r"Each clay robot costs (\d+) ore. "
               r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
               r"Each geode robot costs (\d+) ore and (\d+) obsidian.")

    time_limit = 24
    if part == 2:
        data = data[:3]
        time_limit = 32

    blueprints = {}
    for line in data:
        match = re.match(pattern, line)
        bid = int(match.group(1))
        ore_robot = int(match.group(2)), 0, 0
        clay_robot = int(match.group(3)), 0, 0
        obsidian_robot = int(match.group(4)), int(match.group(5)), 0
        geode_robot = int(match.group(6)), 0, int(match.group(7))
        blueprints[bid] = Blueprint(bid, ore_robot, clay_robot, obsidian_robot, geode_robot, time_limit)

    geodes = []
    with multiprocessing.Pool(3) as pool:
        for result in pool.imap_unordered(get_optimum_geodes, blueprints.values()):
            geodes.append(result)

    if part == 1:
        answer = sum(x[1] for x in geodes)
        # print(f"Part 1 done with answer {answer}")
    else:
        assert part == 2
        answer = math.prod(x[0] for x in geodes)

    return answer


def main():
    data = read_data()
    answer1 = day(data, part=1)
    answer2 = day(data, part=2)
    # answer2 = None
    return answer1, answer2


expected_answers = 1356, 27720
