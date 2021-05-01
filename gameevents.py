import sys
import pygame


def handleEvents(events, game, state):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game.isValidMove():
                x, y = game.makeMove(state.currentPlayer)
                game.showMatrix()
                game.matrix[y][x] = state.currentPlayer[0]
                print(game.text)

                game.solution = game.findSolution()
                if not game.gameOver():
                    state.currentPlayer = game.otherPlayer(state.currentPlayer)
                else:
                    game.text = 'Game over! {} wins!'.format(state.currentPlayer.capitalize())
