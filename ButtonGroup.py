class ButtonGroup:

    def __init__(self, buttonList=None, selected=0, space=70, top=0, left=0):
        if buttonList is None:
            buttonList = []
        self.buttonList = buttonList
        self.selected = selected
        self.buttonList[self.selected].selected = True
        self.top = top
        self.left = left

        currentLeft = self.left
        for button in self.buttonList:
            button.top = self.top
            button.left = currentLeft
            button.updateRectangle()
            currentLeft += space + button.width

    def selectByCoord(self, coord):
        for btnIndex, button in enumerate(self.buttonList):
            if button.selectByCoord(coord):
                self.buttonList[self.selected].select(False)
                self.selected = btnIndex
                return True
        return False

    def draw(self):
        for button in self.buttonList:
            button.draw()

    def getValue(self):
        return self.buttonList[self.selected].value
