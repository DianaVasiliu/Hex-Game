import pygame


def drawTile(display, game, tile):
    corners = tile.cornerPoints(game.boardPosition)
    pygame.draw.polygon(display, tile.colour, corners)
    pygame.draw.polygon(display, (50, 50, 50), corners, 8)
    pygame.draw.polygon(display, (255, 255, 255), corners, 3)


def drawBoard(display, game):
    display.fill(game.backgroundColor)
    for tile in game.hexTiles():
        drawTile(display, game, tile)
    game.showText()
    pygame.display.flip()
