#!/usr/bin/env python
from collections import defaultdict

from AdventOfCode import read_data


def part1(lines):
    """
    Find the number of paths between the 'you' and 'out' nodes in the puzzle input.

    This function requires that there are not any circular paths in the puzzle input.
    """
    # The method is to walk through the outputs of any nodes with no inputs, and add the current
    # node's path count to those output nodes while removing the current node from the output
    # node's input list.  Once a node has no inputs, then its path count is known and its outputs
    # can then be walked.
    nodes = defaultdict(lambda: {'in': [], 'paths': 0})
    for line in lines:
        name, outputs = line.split(': ')
        nodes[name]['out'] = outputs.split()
        for out_name in nodes[name]['out']:
            nodes[out_name]['in'].append(name)
    nodes['you']['paths'] = 1

    actives = [k for k, v in nodes.items() if len(v['in']) == 0]
    while actives:
        name = actives.pop()
        node = nodes[name]
        for out_name in node['out']:
            out_node = nodes[out_name]
            out_node['paths'] += node['paths']
            out_node['in'].remove(name)
            if len(out_node['in']) == 0 and out_name != 'out':
                actives.append(out_name)

    return nodes['out']['paths']


def part2(lines):
    """
    Find the number of paths between the 'svr' and 'out' nodes that pass through both 'dac' and 'fft'.

    This function requires that there are not any circular paths in the puzzle input.
    """
    # The method here is similar to part1, except that we have separate counts for having passed through 'dac', 'fft',
    # both, and neither.  At the 'dac' and 'fft' nodes, all incoming paths count towards the two path counts with
    # 'dac' or 'fft' respectively.
    nodes = defaultdict(lambda: {'in': [],
                                 'paths': 0,
                                 'paths_dac': 0,
                                 'paths_fft': 0,
                                 'paths_both': 0})
    for line in lines:
        name, outputs = line.split(': ')
        nodes[name]['out'] = outputs.split()
        for node in nodes[name]['out']:
            nodes[node]['in'].append(name)
    nodes['svr']['paths'] = 1

    actives = [k for k, v in nodes.items() if len(v['in']) == 0]
    while actives:
        name = actives.pop()
        node = nodes[name]
        for out_name in nodes[name]['out']:
            out_node = nodes[out_name]
            out_node['paths'] += node['paths']
            out_node['paths_dac'] += node['paths_dac']
            out_node['paths_fft'] += node['paths_fft']
            out_node['paths_both'] += node['paths_both']
            if out_name == 'dac':
                out_node['paths_dac'] += node['paths']
                out_node['paths_both'] += node['paths_fft']
                # The incoming 'paths_dac' must be zero because there aren't any circular paths, so no need to add it.
            elif out_name == 'fft':
                out_node['paths_fft'] += node['paths']
                out_node['paths_both'] += node['paths_dac']

            out_node['in'].remove(name)
            if len(out_node['in']) == 0 and out_name != 'out':
                actives.append(out_name)

    return nodes['out']['paths_both']


def main():
    lines = read_data()
    return part1(lines), part2(lines)


expected_answers = 508, 315116216513280
