#!/usr/bin/env python

from functools import cache

from .days import read_data


def part1():
    def roll_die(last_roll, times):
        sum = 0
        for d in range(times):
            last_roll = (last_roll + 1) % 100
            sum += last_roll + 1
        return last_roll, sum

    lines = read_data('day21.data')
    players = {}
    for line in lines:
        if 'Player ' in line:
            p = int(line[7:].split()[0])
            players[p] = {'position': int(line.split()[-1]), 'score': 0}

    goal = 1000
    rolls = 0
    last_roll = 99
    # Starting conditions done.

    while max([p['score'] for p in players.values()]) < goal:
        for player in sorted(players.keys()):
            player = players[player]
            last_roll, value = roll_die(last_roll, 3)
            player['position'] = player['position'] + value
            while player['position'] > 10:
                player['position'] -= 10
            rolls += 3
            player['score'] += player['position']
            if player['score'] >= goal:
                break

    losing_score = min([p['score'] for p in players.values()])
    print(f"Answer for day 21 part 1: {losing_score * rolls}")


def part2():
    @cache
    def get_rolls_to_win(old_pos, old_score, goal):
        """
        Get how many rolls are needed to win, and how many possibilities there are for that roll count.

        :param old_pos: The starting position of the player on the board.
        :param old_score: The starting core of the player.
        :return: {rollCount: WinCount}
        """
        if old_score >= goal:
            # The game is over, so return indicating that zero rolls were needed with one win.
            return {0: 1}

        counts = {}
        # The die is rolled three times to make one movement on the board.
        for roll1 in [1, 2, 3]:
            for roll2 in [1, 2, 3]:
                for roll3 in [1, 2, 3]:
                    roll = roll1 + roll2 + roll3
                    # Calc new position and score for this version of reality.
                    pos = old_pos + roll
                    while pos > 10:
                        pos -= 10
                    score = old_score + pos
                    # Get the roll/win counts possible from here.
                    new_counts = get_rolls_to_win(pos, score, goal)
                    for k, v in new_counts.items():
                        k = k + 3   # The +3 is because we just did three rolls to get here.
                        counts[k] = counts.get(k, 0) + v
        return counts

    def universe_wins_at(player, other_player, roll_count):
        """
        Return the number of universes where this player could have won at this roll count.
        This assumes that player goes ahead of other_player.

        :param player: The roll:win_paths dict for this player.
        :param other_player: The roll:win_paths dict for the other player.
        :param roll_count: How many times the die was rolled by this player before winning.
        :return: The number of possible universes.
        """
        # The other player created many universes along the way. For a single path for this player to win at roll R,
        # the other player could have created as many as (3^R-1) universes.
        # The -3 on the roll_count is because other player is 3 rolls behind this player.
        return player[roll_count] * paths_not_yet_won(other_player, roll_count-3)

    def paths_not_yet_won(player, roll_count):
        """
        Return the number of paths after roll_count rolls where this player has to still be playing (i.e. not won yet).

        :param player: The roll,win_paths dict for this player.
        :param roll_count: How many times the die has been rolled.
        :return: The count of paths in progress.
        """

        if roll_count == 0:
            return 1
        # Each roll of the die creates three paths for each previous path, but some new paths may have won.
        return (3 * paths_not_yet_won(player, roll_count-1)) - player.get(roll_count, 0)

    goal = 21
    p1wins = get_rolls_to_win(6, 0, goal)
    p2wins = get_rolls_to_win(2, 0, goal)

    uni_wins = 0
    for roll in p1wins:
        uni_wins += universe_wins_at(p1wins, p2wins, roll)
    print(f"Answer for day 21 part2: {uni_wins}")


def main():
    part1()
    part2()
