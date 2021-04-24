import sys
import pygame


def handleEvents(events, game):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game.isValidMove():
                x, y = game.makeMove()
                game.showMatrix()
                game.matrix[y][x] = game.currentPlayer[0]
                game.currentPlayer = game.otherPlayer(game.currentPlayer)
                print(game.text)
