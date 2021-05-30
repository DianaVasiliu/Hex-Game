from Game import Game
import pygame


def handleEvents(events, game, state):
    for event in events:
        if event.type == pygame.QUIT:
            Game.running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1 and pos[0] >= 1100 and pos[1] <= 70:
                Game.running = False
                break
            if event.button == 1 and game.isValidMove(state.currentPlayer):
                x, y = game.makeMove(state.currentPlayer)
                game.showMatrix()
                game.matrix[y][x] = state.currentPlayer[0]

                game.solution = game.findSolution()
                if not game.gameOver():
                    state.currentPlayer = game.otherPlayer(state.currentPlayer)
                else:
                    game.text = 'Game over! {} wins!'.format(state.currentPlayer.capitalize())
                return True
    return False
