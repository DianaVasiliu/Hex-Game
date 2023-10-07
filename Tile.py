import helper
import math


class Tile:

    def __init__(self, row, column, size):
        self.gridPosition = (row, column)
        self.width, self.height = helper.computeTileDimensions(size)
        self.neighbours = []

    def __str__(self):
        return f'HexTile{self.gridPosition}'

    def __repr__(self):
        return f'HexTile{self.gridPosition}'

    def centerPoint(self, offset=(0, 0)):
        x, y = self.gridPosition
        dx, dy = offset
        height = math.floor(self.height * 3 / 4)

        if y % 2:
            dx += self.width // 2
        x += y // 2
        return x * self.width + dx, y * height + dy

    def cornerPoints(self, offset=(0, 0)):
        radius = self.height // 2
        position_px = self.centerPoint(offset)
        return [helper.cornerPoint(radius, i, position_px) for i in range(6)]

    def distanceSq(self, position, offset):
        p1 = self.centerPoint(offset)
        p2 = position
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x1 - x2, y2 - y1
        return dx * dx + dy * dy
