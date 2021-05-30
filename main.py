import copy
import pygame
import time
from statistics import mean, median
import helper
import algorithms as alg
from Game import Game
from State import State
import gameevents


def pvp_game_loop():
    playerMoves = [0, 0]
    i = 0
    startTime = int(round(time.time() * 1000))

    while Game.running:
        hexgame.drawBoard()
        events = pygame.event.get()
        doneTurn = gameevents.handleEvents(events, hexgame, currentState)
        if doneTurn:
            endTime = int(round(time.time() * 1000))
            Game.currentPlayer = Game.otherPlayer(Game.currentPlayer)
            playerMoves[i] += 1
            print('Player has thought for {} miliseconds'.format(endTime - startTime))
            print()
            print(hexgame.text)
            i = (i + 1) % 2

    return playerMoves, int(round(time.time() * 1000))


def pvc_game_loop():
    playerMoves = 0
    computerMoves = 0
    computerThinkingTimes = []

    startTime = int(round(time.time() * 1000))

    while Game.running:
        if currentState.currentPlayer == Game.JMIN:
            hexgame.drawBoard()
            events = pygame.event.get()
            doneTurn = gameevents.handleEvents(events, hexgame, currentState)
            if doneTurn:
                endTime = int(round(time.time() * 1000))
                Game.currentPlayer = Game.otherPlayer(Game.currentPlayer)
                playerMoves += 1
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
                updatedState = alg.alpha_beta(-500, 500, currentState)

            endTime = int(round(time.time() * 1000))
            computerMoves += 1
            Game.currentPlayer = Game.otherPlayer(Game.currentPlayer)
            print('The computer\'s estimation:', updatedState.score)
            print('Computer has thought for {} miliseconds'.format(endTime - startTime))
            computerThinkingTimes.append(endTime - startTime)

            currentState.board = updatedState.chosenState.board
            hexgame.emptyTiles -= 1

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

    return playerMoves, computerMoves, computerThinkingTimes, int(round(time.time() * 1000))


if __name__ == '__main__':

    programStartTime = int(round(time.time() * 1000))

    pygame.init()
    icon = pygame.image.load('hex.png')
    pygame.display.set_caption("Hex Game © Gunterina")
    pygame.display.set_icon(icon)

    hexgame = Game()
    display = pygame.display.set_mode(size=hexgame.screenSize)

    hexgame.initialiseGame(display, hexgame)

    Game.JMIN, algorithm, difficulty, gameType = helper.homePage(hexgame, display)
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

    computerThinkingTimes = []
    playerMoves = 0
    computerMoves = 0
    Game.currentPlayer = 'red'

    if gameType == 'pvp':
        playerMoves, programFinalTime = pvp_game_loop()
        print("The Red player moved {} times.".format(playerMoves[0]))
        print("The Blue player moved {} times.".format(playerMoves[1]))
    else:
        playerMoves, computerMoves, computerThinkingTimes, programFinalTime = pvc_game_loop()

        if not computerThinkingTimes:
            computerThinkingTimes = [0]

        print()
        print("Minimum computer think time:", min(computerThinkingTimes))
        print("Maximum computer think time:", max(computerThinkingTimes))
        print("Medium computer think time:", mean(computerThinkingTimes))
        print("Median of computer think time:", median(computerThinkingTimes))
        print()
        print("The player moved {} times.".format(playerMoves))
        print("The computer moved {} times.".format(computerMoves))

    print()
    print("The program has run for {} miliseconds.".format(programFinalTime - programStartTime))
