import pygame
import helper
from Game import Game


def initialiseGame(game):
    pygame.init()
    pygame.display.set_caption("Hex Game © Gunterina")

    display = pygame.display.set_mode(size=game.screenSize)

    helper.homePage(game, display)


if __name__ == '__main__':
    hexgame = Game()
    initialiseGame(hexgame)
