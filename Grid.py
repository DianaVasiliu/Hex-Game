from Tile import Tile


class Grid:

    def __init__(self, height, width, tileSize):
        self.height = height
        self.width = width
        self.tiles = {(x, y): Tile(x, y, tileSize) for x in range(width) for y in range(height)}
