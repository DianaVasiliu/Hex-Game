import pygame
import helper
from Game import Game
import drawing
import gameevents


def game_loop(game):

    while True:
        events = pygame.event.get()
        gameevents.handleEvents(events, game)
        drawing.drawBoard(display, game)


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

    print('Start')
    hexgame.showMatrix()

    print(hexgame.text)

    game_loop(hexgame)
