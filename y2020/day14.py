#!/usr/bin/env python

from AdventOfCode import read_data


def part1(data):
    memory = {}
    mask = None
    for line in data:
        if line.startswith('mask'):
            tmp = line[7:]
            mask = int(tmp.replace('X', '1'), 2), int(tmp.replace('X', '0'), 2)
        elif line.startswith('mem'):
            address, value = line[4:].split('] = ')
            memory[address] = (int(value) & mask[0]) | mask[1]

    answer = sum(memory.values())
    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {answer}")
    return answer


def part2(data):
    memory = {}
    for line in data:
        if line.startswith('mask'):
            mask = line[7:]
            floating_bits = mask.count('X')
        elif line.startswith('mem'):
            address, value = line[4:].split('] = ')

            # Convert address to binary string form and apply the mask.
            tmp_addr = ''
            for index, char in enumerate(mask[::-1]):
                if char != '0':
                    tmp_addr = char + tmp_addr
                else:
                    tmp_addr = str(((int(address) >> index) & 1)) + tmp_addr
            # print(f"mask: {mask}\naddr: {address}\nmasked address: {tmp_addr}")
            address = tmp_addr

            # Write all permutations of the address.
            for i in range(1 << floating_bits):
                tmp_addr = address
                for _ in range(floating_bits):
                    x = i & 1
                    i = i >> 1
                    tmp_addr = tmp_addr.replace('X', str(x), 1)
                tmp_addr = int(tmp_addr, 2)
                # print(f"Writing addr {tmp_addr} = {int(value)}")
                memory[tmp_addr] = int(value)

    answer = sum(memory.values())
    # print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {answer}")
    return answer


def main():
    data = read_data()
    answer1 = part1(data)
    answer2 = part2(data)
    return answer1, answer2


expected_answers = 7817357407588, 4335927555692
