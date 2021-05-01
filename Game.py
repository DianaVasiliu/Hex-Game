import copy
import sys
import pygame.mouse
from Grid import Grid


class Game:
    JMIN = None
    JMAX = None
    EMPTY = '.'
    MAX_DEPTH = 1

    def __init__(self, matrix=None):
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

        self.emptyTiles = self.NUM_ROWS * self.NUM_COLS

        # colours
        self.emptyColour = (70, 70, 70)
        self.playerColours = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255)
        }

        for tile in self.hexTiles():
            tile.colour = self.emptyColour

        self.matrix = matrix or [[self.__class__.EMPTY for _ in range(self.NUM_COLS)] for _ in range(self.NUM_ROWS)]
        self.text = 'Red\'s turn'
        self.solution = None

    @classmethod
    def initialiseGame(cls, display, game):
        cls.display = display
        cls.tileSize = game.tileSize

    def hexTiles(self):
        return self.grid.tiles.values()

    def showMatrix(self):
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if j == 0:
                    print(' ' * i, end='')
                print(str(row[j]), end=' ')
            print()

    @classmethod
    def otherPlayer(cls, player):
        if player == cls.JMIN:
            return cls.JMAX
        return cls.JMIN

    def showText(self):
        fontObj = pygame.font.SysFont('arial', 40)
        renderedText = fontObj.render(self.text, True, (255, 255, 255))
        width = 400
        height = 100
        left = self.screenSize[0] / 2 - width / 2
        top = self.screenSize[1] - 1.3*height
        rectangle = pygame.Rect(left, top, width, height)
        rectangleText = renderedText.get_rect(center=rectangle.center)
        pygame.draw.rect(self.display, (0, 0, 0), rectangle)
        self.display.blit(renderedText, rectangleText)

    def makeMove(self, player):
        tile = self.getNearestTile(pygame.mouse.get_pos())
        tile.colour = self.playerColours[player]

        x, y = tile.gridPosition
        self.matrix[y][x] = player[0].upper()
        self.grid.visitedTiles[tile.gridPosition] = 1
        self.emptyTiles -= 1

        otherPlayer = self.otherPlayer(player)
        self.text = otherPlayer.capitalize() + '\'s turn'
        self.solution = self.findSolution()

        if self.solution is not None:
            self.text = 'Game over! {} wins!'.format(player.capitalize())
        elif self.solution is None and self.emptyTiles == 0:
            self.text = 'Game over! It\'s a tie!'

        return x, y

    def getNearestTile(self, pos):
        nearestTile = None
        minDist = sys.maxsize

        for tile in self.hexTiles():
            distance = tile.distanceSq(pos, self.boardPosition)
            if distance < minDist:
                minDist = distance
                nearestTile = tile
        return nearestTile

    def nextMoves(self, player):
        moves = []
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLS):
                if self.matrix[i][j] == self.EMPTY:
                    newMatrix = copy.deepcopy(self.matrix)
                    newMatrix[i][j] = player[0].upper()
                    newGame = Game(newMatrix)
                    newGame.currentPlayer = self.otherPlayer(player)
                    newGame.text = newGame.currentPlayer.capitalize() + '\'s turn'
                    moves.append(newGame)
        return moves

    def isValidMove(self):
        if self.gameOver():
            return False
        tile = self.getNearestTile(pygame.mouse.get_pos())
        return self.matrix[tile.gridPosition[1]][tile.gridPosition[0]] == self.EMPTY

    def estimateScore(self, depth):
        # TODO
        return depth

    def gameOver(self):
        if self.solution is None:
            self.findSolution()
        return self.solution is not None

    def findSolution(self):
        for tile in self.grid.topRow():
            if tile.colour == self.playerColours['red']:
                path = self.grid.findPath(
                    tile,
                    self.grid.bottomRow(),
                    self.playerColours['red']
                )

                if path is not None:
                    return path

        for tile in self.grid.leftColumn():
            if tile.colour == self.playerColours['blue']:
                path = self.grid.findPath(
                    tile,
                    self.grid.rightColumn(),
                    self.playerColours['blue']
                )

                if path is not None:
                    return path

        return None

    # drawing methods
    def drawTile(self, tile):
        corners = tile.cornerPoints(self.boardPosition)
        pygame.draw.polygon(self.display, tile.colour, corners)
        pygame.draw.polygon(self.display, (50, 50, 50), corners, 5)
        pygame.draw.polygon(self.display, (255, 255, 255), corners, 3)

    def drawBoard(self):
        self.display.fill(self.backgroundColor)
        for tile in self.hexTiles():
            self.drawTile(tile)
        self.showText()

        if self.solution is not None:
            self.drawPath()

        self.drawBorder()

        pygame.display.flip()

    def drawPath(self):
        path = self.solution

        for tile in path:
            pygame.draw.polygon(self.display, color=(0, 0, 0), points=tile.cornerPoints(self.boardPosition), width=7)

    def drawBorder(self):
        colours = list(self.playerColours.values())
        colour1 = colours[0]
        colour2 = colours[1]
        width = 4

        self.drawOneSideBorder(colour1, self.grid.topRow(), 3, 6, width)
        self.drawOneSideBorder(colour1, self.grid.bottomRow(), 0, 3, width)
        self.drawOneSideBorder(colour2, self.grid.leftColumn(), 1, 4, width)
        self.drawOneSideBorder(colour2, self.grid.rightColumn(), 4, 1, width)

    def drawOneSideBorder(self, colour, row, fromPoint, toPoint, width):
        for tile in row:
            corners = tile.cornerPoints(self.boardPosition)
            if fromPoint >= toPoint:
                corners = corners[fromPoint:] + corners[:toPoint]
            else:
                corners = corners[fromPoint:toPoint]
            pygame.draw.lines(self.display, color=colour, points=corners, width=width, closed=False)
