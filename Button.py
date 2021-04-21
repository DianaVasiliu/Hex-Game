import pygame.font


class Button:

    def __init__(self, display=None, top=0, left=0, w=0, h=0,
                 bgColor=(255, 204, 153), selectedBgColor=(255, 128, 0),
                 text='', font='arial', fontDimension=36,
                 textColor=(0, 0, 0), value=''):
        self.display = display
        self.bgColor = bgColor
        self.selectedBgColor = selectedBgColor
        self.text = text
        self.font = font
        self.width = w
        self.height = h
        self.selected = False
        self.fontDimension = fontDimension
        self.textColor = textColor
        self.top = top
        self.left = left

        fontObj = pygame.font.SysFont(self.font, self.fontDimension)
        self.renderedText = fontObj.render(self.text, True, self.textColor)
        self.rectangle = pygame.Rect(left, top, w, h)
        self.rectangleText = self.renderedText.get_rect(center=self.rectangle.center)
        self.value = value

    def select(self, selected):
        self.selected = selected
        self.draw()

    def selectByCoord(self, coord):
        if self.rectangle.collidepoint(coord):
            self.select(True)
            return True
        return False

    def updateRectangle(self):
        self.rectangle.left = self.left
        self.rectangle.top = self.top
        self.rectangleText = self.renderedText.get_rect(center=self.rectangle.center)

    def draw(self):
        if self.selected:
            bgColor = self.selectedBgColor
        else:
            bgColor = self.bgColor

        pygame.draw.rect(self.display, bgColor, self.rectangle)
        self.display.blit(self.renderedText, self.rectangleText)