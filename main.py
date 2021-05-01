import copy
import pygame
import time
import helper
import algorithms as alg
from Game import Game
from State import State
import gameevents


if __name__ == '__main__':
    pygame.init()
    icon = pygame.image.load('hex.png')
    pygame.display.set_caption("Hex Game © Gunterina")
    pygame.display.set_icon(icon)

    hexgame = Game()
    display = pygame.display.set_mode(size=hexgame.screenSize)

    hexgame.initialiseGame(display, hexgame)

    Game.JMIN, algorithm, difficulty = helper.homePage(hexgame, display)
    Game.JMAX = 'red' if Game.JMIN == 'blue' else 'blue'

    if difficulty == 'beginner':
        Game.MAX_DEPTH = 1
    elif difficulty == 'medium':
        Game.MAX_DEPTH = 2
    elif difficulty == 'advanced':
        Game.MAX_DEPTH = 3

    print('Start')
    hexgame.showMatrix()

    print(hexgame.text)

    currentState = State(hexgame, 'red', hexgame.MAX_DEPTH)

    startTime = int(round(time.time() * 1000))
    while True:

        if currentState.currentPlayer == Game.JMIN:
            hexgame.drawBoard()
            events = pygame.event.get()
            doneTurn = gameevents.handleEvents(events, hexgame, currentState)
            if doneTurn:
                endTime = int(round(time.time() * 1000))
                print('Player has thought for {} miliseconds'.format(endTime - startTime))
                print()
                print(hexgame.text)
        else:
            hexgame.drawBoard()

            startTime = int(round(time.time() * 1000))

            currentState.board.matrix = copy.deepcopy(hexgame.matrix)
            if algorithm == 'minimax':
                updatedState = alg.minimax(currentState)
            else:
                pass
                # updatedState = alg.alpha_beta(-500, 500, currentState)

            endTime = int(round(time.time() * 1000))
            print('Computer has thought for {} miliseconds'.format(endTime - startTime))

            currentState.board = updatedState.chosenState.board

            hexgame.matrix = copy.deepcopy(currentState.board.matrix)
            hexgame.showMatrix()

            for i in range(len(hexgame.matrix)):
                for j in range(len(hexgame.matrix[i])):
                    if hexgame.matrix[i][j] == hexgame.JMAX[0].upper():
                        for tile in hexgame.hexTiles():
                            if tile.gridPosition == (j, i):
                                tile.colour = hexgame.playerColours[hexgame.JMAX]
                                hexgame.matrix[i][j] = hexgame.JMAX[0].lower()

            hexgame.solution = hexgame.findSolution()

            if not hexgame.gameOver():
                hexgame.text = '{}\'s turn'.format(hexgame.JMIN.capitalize())
            else:
                hexgame.text = 'Game over! {} wins!'.format(hexgame.JMAX.capitalize())

            print(hexgame.text)

            currentState.currentPlayer = Game.otherPlayer(currentState.currentPlayer)
            startTime = int(round(time.time() * 1000))
