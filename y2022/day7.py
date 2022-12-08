#!/usr/bin/env python

from AdventOfCode import read_data


def day(data):
    # Keep a list of the current directory stack.  When encountering a file, add size to all directories in the stack.
    directory_sizes = {}
    current_directories = []
    current_command = None

    for line in data:
        if line.startswith("$"):
            # Parse commands.
            cmd = line[2:].split(' ')
            # print(f"Command:", cmd)
            if cmd[0] == "cd":
                current_command = "cd"
                folder = cmd[1]
                if folder == '/':
                    current_directories = ['/']
                elif folder == '..':
                    del current_directories[-1]
                else:
                    folder = current_directories[-1] + '/' + folder
                    current_directories.append(folder)
                # print(f"New directories: {current_directories}")
            elif cmd[0] == "ls":
                current_command = "ls"
                assert current_directories[-1] not in directory_sizes
            else:
                raise AssertionError(f"Unknown command {cmd}")
        else:
            # We must be in the output of 'ls'.
            assert current_command == "ls"
            line = line.split(' ')
            if line[0] == 'dir':
                # Nothing to do here yet.
                continue
            else:
                assert line[0].isnumeric()
                size = int(line[0])
                filename = line[1]
                # Add size to all directories in the structure.
                # print(f"Adding {size} to {current_directories}")
                for folder in current_directories:
                    if folder not in directory_sizes:
                        directory_sizes[folder] = 0
                    directory_sizes[folder] += int(size)

    # Part 1 question: what is the total size of directories which have a size of at most 100000.
    total = 0
    for folder, size in directory_sizes.items():
        if size <= 100_000:
            total += size
    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 1: {total}")

    # Part 2: What is the smallest single directory that can be deleted to free up enough space?
    # First figure out how much space is needed.
    disk_size = 70000000
    required_space = 30000000
    free_space = disk_size - directory_sizes['/']
    min_deletion = required_space - free_space

    # Loop through all entries to find the one with the smallest excess size.
    best_diff = 999999999999999
    best_folder = None
    for folder, size in directory_sizes.items():
        if size < min_deletion:
            continue
        delta = size - min_deletion
        if delta < best_diff:
            best_diff = delta
            best_folder = folder, size

    print(f"Answer for {__name__[1:5]} day {__name__[9:]} part 2: {best_folder[1]}")


def main():
    data = read_data(__file__)
    day(data)
