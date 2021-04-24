import sys
import pygame


def handleEvents(events, game):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('Move')
                # game.makeMove()
