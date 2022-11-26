#!/usr/bin/env python

from . import read_data


class Image:
    def __init__(self, pixels, missing_pixels=0):
        # pixel is x,y format, where +x is to the right and +y is down.
        self.missing_pixel = missing_pixels
        # A value of 1 means the pixel is lit, 0 means dark.
        self.pixels = pixels

    def display(self):
        """ Print the image. """

        x_min = min([x for x, y in self.pixels.keys()])
        x_max = max([x for x, y in self.pixels.keys()])
        y_min = min([y for x, y in self.pixels.keys()])
        y_max = max([y for x, y in self.pixels.keys()])

        print("\nWidth: ", x_max - x_min + 1)
        print("Height: ", y_max - y_min + 1)
        for y in range(y_min-1, y_max+2):
            row = ''
            for x in range(x_min-1, x_max+2):
                row += '#' if self.get_pixel((x, y)) else '.'
            print(row)

    def get_pixel(self, pixel):
        """ Return the pixel (1 == lit, 0 == dark) from anywhere in the infinite image. """
        return self.pixels.get(pixel, self.missing_pixel)

    def get_neighbor_code(self, pixel):
        """
        Read the image around the specified pixel. From the neighbor pixels, make the index into the enhancement algo.
        :return: The index number for the specified pixel.
        """

        neigh_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        x, y = pixel

        index = 0
        for dx, dy in neigh_offsets:
            index = (index << 1) + self.get_pixel((x+dx, y+dy))
        return index

    def get_enhanced_image(self, algo):
        """ Return a new Image object which has been enhanced by the algorithm. """
        new_missing = algo[self.missing_pixel]
        x_min = min([x for x, y in self.pixels.keys()])
        x_max = max([x for x, y in self.pixels.keys()])
        y_min = min([y for x, y in self.pixels.keys()])
        y_max = max([y for x, y in self.pixels.keys()])

        new_pixels = {}
        for y in range(y_min-1, y_max+2):
            for x in range(x_min-1, x_max+2):
                p = algo[self.get_neighbor_code((x, y))]
                if p != new_missing:
                    # We don't need to include a pixel if it's already the default, so skip it for a slight speedup.
                    new_pixels[(x, y)] = p

        new_img = Image(new_pixels, missing_pixels=new_missing)
        return new_img

    def count_lit_pixels(self):
        """ Return the count of pixels that are lit. """
        if self.missing_pixel == 1:
            return float('inf')
        return sum([p for p in self.pixels.values()])


def main():
    lines = read_data('day20.data')
    # lines = read_data('day20_test.data')
    algorithm = lines[0]
    algorithm = algorithm.replace('.', '0')
    algorithm = algorithm.replace('#', '1')
    algorithm = [int(x) for x in algorithm]

    pixels = {}
    y = 0
    for line in lines[2:]:
        for x, char in enumerate(line):
            # Assume '.' is the background color and only store differing pixels.
            pixels[(x, y)] = 1 if char == '#' else 0
        y += 1
    img = Image(pixels, missing_pixels=0)
    # Initial image constructed.

    for _ in range(2):
        img = img.get_enhanced_image(algorithm)
    print(f"Answer for 2021 day 20 part 1:", img.count_lit_pixels())

    for _ in range(48):
        img = img.get_enhanced_image(algorithm)
    print(f"Answer for 2021 day 20 part 2:", img.count_lit_pixels())
