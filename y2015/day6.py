#!/usr/bin/env python3

from AdventOfCode import read_data

TOGGLE = "toggle"


class XmasLights:
    def __init__(self, size):
        self.size = size
        self.sections = {(0, 0, size-1, size-1): 0}

    def sum_brightness(self):
        """ Return the total brightness of the lights. """
        on = 0
        off = 0
        light = 0
        for rect, brightness in self.sections.items():
            if brightness == 0:
                off += (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1)
            else:
                on += (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1)
                light += (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1) * brightness
        assert on + off == self.size**2
        return light

    @staticmethod
    def split_rect(rect, x=None, y=None):
        """
        Split the given rect at the given location and return the two new rects.

        The split axis will be included in the rect with the lower values.
        """
        rect1 = list(rect)
        rect2 = list(rect)
        if x is not None:
            assert rect[0] <= x < rect[2]
            rect1[2] = x
            rect2[0] = x+1
        if y is not None:
            assert rect[1] <= y < rect[3]
            rect1[3] = y
            rect2[1] = y+1
        return tuple(rect1), tuple(rect2)

    def split_rects(self, splittee, splitter):
        """
        Split rect_to_split at an edge of rect_other, then return the two new rects.

        There must be partial overlap between the two rects, meaning that neither rect fully covers the other and there
        at least some overlap.
        """
        split_x, split_y = None, None
        if splittee[0] < splitter[0]:
            split_x = splitter[0] - 1
        elif splittee[2] > splitter[2]:
            split_x = splitter[2]
        elif splittee[1] < splitter[1]:
            split_y = splitter[1] - 1
        else:
            assert splittee[3] > splitter[3]
            split_y = splitter[3]
        return self.split_rect(splittee, x=split_x, y=split_y)

    def add_section(self, new_rect, action):
        new_rect = tuple(new_rect)
        min_x, min_y, max_x, max_y = new_rect
        perfect_match = False
        stack = list(self.sections.keys())
        while stack:
            rect = stack.pop()
            old_lit = self.sections[rect]

            if rect[0] > max_x or rect[1] > max_y or rect[2] < min_x or rect[3] < min_y:
                # No overlap.
                continue
            elif new_rect == rect:
                # Perfect overlap.  Update the current lit value and don't add the new rect at the end.
                old_lit = self.sections[rect]
                self.sections[rect] = action if action is not TOGGLE else old_lit ^ 1
                perfect_match = True
                break
            elif rect[0] >= min_x and rect[1] >= min_y and rect[2] <= max_x and rect[3] <= max_y:
                # New rect fully covers old rect.
                if action is TOGGLE:
                    self.sections[rect] = old_lit ^ 1
                else:
                    # Delete the underlying rect, as a new one covering this will be added later.
                    del self.sections[rect]
            else:
                # Partial overlap.  Split the underlying rect at one of the edges.
                self.sections.pop(rect)
                for tmp_rect in self.split_rects(rect, new_rect):
                    self.sections[tmp_rect] = old_lit
                    stack.append(tmp_rect)

        if not perfect_match and action is not TOGGLE:
            self.sections[new_rect] = action

    def add_section_part2(self, new_rect, delta):
        new_rect = tuple(new_rect)
        min_x, min_y, max_x, max_y = new_rect
        stack = list(self.sections.keys())
        while stack:
            rect = stack.pop()
            bright = self.sections[rect]

            if rect[0] > max_x or rect[1] > max_y or rect[2] < min_x or rect[3] < min_y:
                # No overlap.
                continue
            elif new_rect == rect:
                # Perfect overlap.  Update the current brightness value.
                self.sections[rect] = max(0, bright + delta)
                break
            elif rect[0] >= min_x and rect[1] >= min_y and rect[2] <= max_x and rect[3] <= max_y:
                # New rect fully covers old rect.
                self.sections[rect] = max(0, bright + delta)
            else:
                # Partial overlap.  Split the underlying rect at one of the edges.
                self.sections.pop(rect)
                for tmp_rect in self.split_rects(rect, new_rect):
                    self.sections[tmp_rect] = bright
                    stack.append(tmp_rect)


def fast(lines, part=1):
    size = 1_000
    lights = XmasLights(size=size)
    for line in lines:
        line = line.replace(" through ", ",")
        action_str, rect_str = line.rsplit(' ', 1)
        rect = [int(x) for x in rect_str.split(',')]
        action_str = action_str.strip()
        if part == 1:
            if action_str == "turn on":
                action = 1
            elif action_str == "turn off":
                action = 0
            else:
                assert action_str == "toggle"
                action = TOGGLE
        else:
            if action_str == "turn on":
                action = 1
            elif action_str == "turn off":
                action = -1
            else:
                assert action_str == "toggle"
                action = + 2

        # count0 = len(lights.sections)
        if part == 1:
            lights.add_section(rect, action)
        else:
            lights.add_section_part2(rect, action)
        # count1 = len(lights.sections)
        # print(f"Current rect count: {count1} (delta {count1 - count0})")
        # print(f"Sum {part=} is {lights.sum_brightness()} after '{line}'")

    return lights.sum_brightness()


def part1_alt(lines):
    lights = [[0 for y in range(0, 1000)] for x in range(0, 1000)]
    for line in lines:
        line = line.replace(" through ", ",")
        action_str, rect_str = line.rsplit(' ', 1)
        action_str = action_str.strip()
        if action_str == "turn on":
            action = 1
        elif action_str == "turn off":
            action = 0
        else:
            assert action_str == "toggle"
            action = TOGGLE

        rect = [int(x) for x in rect_str.split(',')]
        xfirst, yfirst, xlast, ylast = rect
        width = ylast - yfirst + 1
        for x, col in enumerate(lights[xfirst:xlast+1], start=xfirst):
            if action in [0, 1]:
                col[yfirst:ylast+1] = [action]*width
            else:
                for y, lit in enumerate(col[yfirst:ylast+1], start=yfirst):
                    col[y] = lit ^ 1

    count = sum([sum(row) for row in lights])
    # print(f"Sum is {count} after '{line}'")
    return count


def part2_alt(lines):
    lights = [[0 for y in range(0, 1000)] for x in range(0, 1000)]
    for line in lines:
        line = line.replace(" through ", ",")
        action_str, rect_str = line.rsplit(' ', 1)
        action_str = action_str.strip()
        if action_str == "turn on":
            action = 1
        elif action_str == "turn off":
            action = -1
        else:
            assert action_str == "toggle"
            action = 2

        rect = [int(x) for x in rect_str.split(',')]
        xfirst, yfirst, xlast, ylast = rect
        for x, col in enumerate(lights[xfirst:xlast+1], start=xfirst):
            for y, lit in enumerate(col[yfirst:ylast+1], start=yfirst):
                col[y] = max(lit + action, 0)

    count = sum([sum(row) for row in lights])
    return count


def main():
    lines = read_data()
    answer1 = fast(lines, part=1)
    answer2 = fast(lines, part=2)
    # answer1 = part1_alt(lines)
    # answer2 = part2_alt(lines)
    return answer1, answer2


expected_answers = (377891, 14110788)
