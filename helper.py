import sys

from Button import *
from ButtonGroup import *

buttonHeight = 50
algButtonWidth = 170
playerButtonWidth = 100
startButtonWidth = 110
topMargin = 50


def homePage(game, display):
    algorithm = ButtonGroup(
        top=topMargin,
        left=game.screenSize[0] / 2 - algButtonWidth,
        buttonList=[
            Button(display=display, w=algButtonWidth, h=buttonHeight, text="Minimax", value="minimax"),
            Button(display=display, w=algButtonWidth, h=buttonHeight, text="Alpha-Beta", value="alphabeta")
        ],
        selected=1
    )
    player = ButtonGroup(
        top=2*topMargin + buttonHeight,
        left=game.screenSize[0] / 2 - playerButtonWidth,
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight, text="Color1", value="color1"),
            Button(display=display, w=playerButtonWidth, h=buttonHeight, text="Color2", value="color2")
        ],
        selected=0
    )
    start = Button(display=display,
                   top=3*topMargin + 2*buttonHeight,
                   left=game.screenSize[0] / 2 - startButtonWidth / 2 + 35,
                   w=startButtonWidth,
                   h=buttonHeight,
                   text="START",
                   bgColor=(0, 230, 115))

    algorithm.draw()
    player.draw()
    start.draw()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not algorithm.selectByCoord(pos):
                    if not player.selectByCoord(pos):
                        if start.selectByCoord(pos):
                            display.fill((0, 0, 0))
                            # currentBoard.drawGrid()
                            return player.getValue(), algorithm.getValue()
        pygame.display.update()



