from Grid import Grid


class Game:
    JMIN = None
    JMAX = None
    EMPTY = '.'

    def __init__(self):
        self.backgroundColor = (0, 0, 0)
        self.screenSize = (1280, 720)
        self.boardPosition = (250, 80)

        self.tileSize = 30
        self.NUM_ROWS = 11
        self.NUM_COLS = 11
        self.grid = Grid(
            self.NUM_ROWS,
            self.NUM_COLS,
            self.tileSize
        )

        # colours
        self.emptyColour = (70, 70, 70)
        self.player1Color = (255, 0, 0)
        self.player2Color = (0, 0, 255)

        for tile in self.hexTiles():
            tile.colour = self.emptyColour

    @classmethod
    def initialiseGame(cls, display, game):
        cls.display = display
        cls.tileSize = game.tileSize

    def hexTiles(self):
        return self.grid.tiles.values()
