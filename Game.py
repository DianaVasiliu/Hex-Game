import copy
import sys
import pygame.mouse
from Grid import Grid
from Button import Button


class Game:
    JMIN = None
    JMAX = None
    EMPTY = '.'
    MAX_DEPTH = 1
    topTile = None
    bottomTile = None
    rightTile = None
    leftTile = None
    currentPlayer = None
    running = True

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

        self.redPath = []
        self.bluePath = []
        self.foundRedPath = 0
        self.foundBluePath = 0

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
        top = self.screenSize[1] - 1.3 * height
        rectangle = pygame.Rect(left, top, width, height)
        rectangleText = renderedText.get_rect(center=rectangle.center)
        pygame.draw.rect(self.display, (0, 0, 0), rectangle)
        self.display.blit(renderedText, rectangleText)

    def makeMove(self, player):
        # luam cel mai apropiat tile de mouse
        tile = self.getNearestTile(pygame.mouse.get_pos())
        # coloram tile-ul in culoarea player-ului
        tile.colour = self.playerColours[player]

        # actualizam caracterul din matrice
        x, y = tile.gridPosition
        self.matrix[y][x] = player[0].upper()
        self.grid.visitedTiles[tile.gridPosition] = 1
        self.emptyTiles -= 1

        # actualizam datele despre jucatorul curent
        otherPlayer = self.otherPlayer(player)
        self.text = otherPlayer.capitalize() + '\'s turn'

        # verifican daca am ajuns la o solutie (daca a castigat vreun jucator)
        self.solution = self.findSolution()

        if self.solution is not None:
            self.text = 'Game over! {} wins!'.format(player.capitalize())
        elif self.solution is None and self.emptyTiles == 0:
            self.text = 'Game over! It\'s a tie!'

        # actualizam tile-urile din pozitii extreme
        if player == 'red':
            if Game.topTile is None:
                Game.topTile = tile.gridPosition
            else:
                if tile.gridPosition[1] < Game.topTile[1]:
                    Game.topTile = tile.gridPosition

            if Game.bottomTile is None:
                Game.bottomTile = tile.gridPosition
            else:
                if tile.gridPosition[1] > Game.bottomTile[1]:
                    Game.bottomTile = tile.gridPosition
        elif player == 'blue':
            if Game.leftTile is None:
                Game.leftTile = tile.gridPosition
            else:
                if tile.gridPosition[0] < Game.leftTile[0]:
                    Game.leftTile = tile.gridPosition

            if Game.rightTile is None:
                Game.rightTile = tile.gridPosition
            else:
                if tile.gridPosition[0] > Game.rightTile[0]:
                    Game.rightTile = tile.gridPosition

        # print('top tile:', self.topTile)
        # print('bottom tile:', self.bottomTile)
        # print('left tile:', self.leftTile)
        # print('right tile:', self.rightTile)
        return x, y

    def getNearestTile(self, pos):
        nearestTile = None
        minDist = sys.maxsize

        for tile in self.hexTiles():
            # calculam distantele de la mouse la toate tile-urile
            distance = tile.distanceSq(pos, self.boardPosition)
            if distance < minDist:
                minDist = distance
                nearestTile = tile
        # returnam cel mai apropiat tile
        return nearestTile

    def nextMoves(self, player):
        # if the player can only move a tile adjacent to another tile
        computerTiles = []
        allTiles = self.grid.tiles
        for i in range(self.NUM_ROWS):
            for j in range(self.NUM_COLS):
                # creem o lista cu toate tile-urile ocupate de calculator
                # cautam in matrice pozitiile pe care a mutat calculatorul
                if self.matrix[i][j] == self.JMAX[0].lower():
                    computerTiles.append(allTiles[(j, i)])

        moves = []
        for computerTile in computerTiles:
            # pentru fiecare tile ocupat de calculator, selectam vecinii
            neighbours = computerTile.neighbours
            for n in neighbours:
                j, i = n.gridPosition
                # pentru fiecare vecin, verificam sa fie liber
                if self.matrix[i][j] == self.EMPTY:
                    # copiem matricea starii curente
                    newMatrix = copy.deepcopy(self.matrix)
                    # in noua matrice, pozitionam culoarea calculatorului
                    newMatrix[i][j] = player[0].upper()
                    # creem o stare noua cu matricea nou formata
                    newGame = Game(newMatrix)
                    newGame.currentPlayer = self.otherPlayer(player)
                    newGame.text = newGame.currentPlayer.capitalize() + '\'s turn'
                    # adaugam aceasta stare noua la lista de mutari
                    moves.append(newGame)

        # if the players can move anywhere on the table
        # moves = []
        # for i in range(self.NUM_ROWS):
        #     for j in range(self.NUM_COLS):
        #         if self.matrix[i][j] == self.EMPTY:
        #             newMatrix = copy.deepcopy(self.matrix)
        #             newMatrix[i][j] = player[0].upper()
        #             newGame = Game(newMatrix)
        #             newGame.currentPlayer = self.otherPlayer(player)
        #             newGame.text = newGame.currentPlayer.capitalize() + '\'s turn'
        #             moves.append(newGame)
        return moves

    def isValidMove(self, player):
        if self.gameOver():
            return False

        tile = self.getNearestTile(pygame.mouse.get_pos())
        # the player can place a tile anywhere
        # return self.matrix[tile.gridPosition[1]][tile.gridPosition[0]] == self.EMPTY

        # the player can only place a tile next to another tile
        allTiles = self.NUM_ROWS * self.NUM_COLS

        # daca toate tile-urile sunt goale (sau una singura a fost ocupata)
        if self.emptyTiles in [allTiles, allTiles - 1]:
            # returnam True daca piesa pe care vrem sa mutam e goala
            # sau false altfel
            return self.matrix[tile.gridPosition[1]][tile.gridPosition[0]] == self.EMPTY

        ok = False
        # verificam ca tile-ul pe care vrem sa mutam are macar un vecin colorat in culoarea player-ului
        for neigh in tile.neighbours:
            c, l = neigh.gridPosition
            if self.matrix[l][c].lower() == player[0]:
                ok = True
                break
        if ok:
            return self.matrix[tile.gridPosition[1]][tile.gridPosition[0]] == self.EMPTY
        return False

    def estimateScore(self, depth):
        # calculam cate mutari mai are de facut RED pana cand creeaza puntea sus-jos
        # calculam cate mutari mai are de facut BLUE pana cand creeaza puntea stanga-dreapta
        # estimarea scorului pentru calculator este scorPlayer - scorCalculator

        # daca scorPlayer - scorCalculator < 0 => scorPlayer < scorCalculator
        # => player-ul e mai aproape de WIN decat calculatorul

        # daca scorPlayer - scorCalculator > 0 => scorPlayer > scorCalculator
        # => calculatorul e mai aproape de WIN decat playerul

        # daca scorPlayer - scorCalculator == 0 => scorPlayer == scorCalculator
        # => player-ul si calculatorul sunt la fel de departe de win

        self.foundRedPath = 0
        self.foundBluePath = 0
        self.redPath = []
        self.bluePath = []
        redPathLength = self.NUM_ROWS
        bluePathLength = self.NUM_COLS
        # if self.topTile:
        #     self.getRedShortestPath(self.grid.tiles[self.topTile])
        #     redPathLength = len(self.redPath)
        # if self.leftTile:
        #     self.getBlueShortestPath(self.grid.tiles[self.leftTile])
        #     bluePathLength = len(self.bluePath)

        # euristica: scor_player - scor_calculator
        if Game.JMAX == 'red':
            return bluePathLength - redPathLength
        else:
            return redPathLength - bluePathLength

    def getRedShortestPath(self, currentTile):
        # if we found both parts of the path, we stop
        if self.foundRedPath == 2:
            return

        allTiles = self.grid.tiles

        # finding the top path part
        if self.topTile is not None:
            # we get the neighbours and rearrange them so we get the top neighbours first
            neighbours = allTiles[currentTile.gridPosition].neighbours
            neighbours.reverse()
            # we filter the neighbours so we have only the available ones
            neighbours = list(filter(lambda tile: self.matrix[tile.gridPosition[1]][tile.gridPosition[0]] == '.',
                                     neighbours))

            for neigh in neighbours:
                # if we have found the top path, we stop searching for the next neighbours
                if self.foundRedPath != 0:
                    break

                # we check if the neighbour is valid (it is empty)
                y, x = neigh.gridPosition[0], neigh.gridPosition[1]
                if self.matrix[x][y] == Game.EMPTY:

                    # print('appended neigh:', neigh)

                    # we add the neighbour to the path
                    self.redPath.append(neigh)
                    # if this neighbour is on the first row, we found the path and we stop the search
                    if neigh.gridPosition[1] == 0:
                        self.foundRedPath += 1
                        break
                    # otherwise, we continue the recursive search into the neighbour
                    self.getRedShortestPath(neigh)
                    # self.redPath.remove(neigh)
            # print(self.redPath)
            # print()

    # def getPlayerShortestPath(self):
    #     return []

    def gameOver(self):
        if self.solution is None:
            self.findSolution()
        return self.solution is not None

    def findSolution(self):
        # cautam path-ul sus-jos incepand de la cea mai de sus piesa rosie (de pe primul rand)
        for tile in self.grid.topRow():
            if tile.colour == self.playerColours['red']:
                path = self.grid.findPath(
                    tile,
                    self.grid.bottomRow(),
                    self.playerColours['red']
                )

                if path is not None:
                    return path

        # cautam path-ul stanga-dreapta incepand de la cea mai din stanga piesa albastra (de pe prima coloana)
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

        # text = str(tile.gridPosition)
        # self.display.blit(pygame.font.SysFont('Arial', 15)
        #                   .render(text, True, (255, 255, 255)), (corners[3], corners[4]))

        if tile == self.getNearestTile(pygame.mouse.get_pos()):
            if not self.gameOver():
                pygame.draw.circle(self.display, color=self.playerColours[self.currentPlayer],
                                   center=tile.centerPoint(self.boardPosition), radius=10)

    def drawBoard(self):
        self.display.fill(self.backgroundColor)
        for tile in self.hexTiles():
            self.drawTile(tile)
        self.showText()

        if self.solution is not None:
            self.drawPath()

        self.drawBorder()

        self.drawQuitButton()

        if Game.running:
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

    def drawQuitButton(self):
        buttonWidth = 150
        buttonHeight = 50
        quitbtn = Button(display=self.display,
                         top=20,
                         left=self.screenSize[0] - buttonWidth - 20,
                         w=buttonWidth,
                         h=buttonHeight,
                         text="QUIT",
                         bgColor=(255, 20, 0))
        quitbtn.draw()
