from Tile import Tile


class Grid:

    def __init__(self, height, width, tileSize):
        self.height = height
        self.width = width
        self.tiles = {(x, y): Tile(x, y, tileSize) for x in range(width) for y in range(height)}
        self.visitedTiles = {(x, y): 0 for x in range(width) for y in range(height)}

        for tile in self.tiles.values():
            self.findNeighbours(tile)

    def findNeighbours(self, tile):
        x, y = tile.gridPosition

        if x > 0:
            tile.neighbours.append(self.tiles[(x - 1, y)])
        if x < self.width - 1:
            tile.neighbours.append(self.tiles[(x + 1, y)])
        if y > 0:
            tile.neighbours.append(self.tiles[(x, y - 1)])
        if y < self.height - 1:
            tile.neighbours.append(self.tiles[(x, y + 1)])

        if x < self.width - 1 and y > 0:
            tile.neighbours.append(self.tiles[(x + 1, y - 1)])
        if x > 0 and y < self.height - 1:
            tile.neighbours.append(self.tiles[(x - 1, y + 1)])

    def topRow(self):
        return [self.tiles[(x, 0)] for x in range(self.width)]

    def bottomRow(self):
        return [self.tiles[(x, self.height - 1)] for x in range(self.width)]

    def leftColumn(self):
        return [self.tiles[(0, y)] for y in range(self.height)]

    def rightColumn(self):
        return [self.tiles[(self.width - 1, y)] for y in range(self.height)]

    def findPath(self, fromTile, toTileList, playerColour, visited=None):
        if visited is None:
            visited = []

        if fromTile.colour != playerColour:
            return None
        if fromTile in visited:
            return None

        if fromTile in toTileList:
            return [fromTile]

        visited.append(fromTile)

        for neighbour in fromTile.neighbours:
            path = self.findPath(neighbour, toTileList, playerColour, visited)
            if path is not None:
                path.append(fromTile)
                return path

        return None
