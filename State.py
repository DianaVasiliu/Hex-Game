from Game import Game


class State:

    def __init__(self, board, currentPlayer, depth, parent=None, score=None):
        self.board = board
        self.currentPlayer = currentPlayer
        self.depth = depth
        self.score = score
        self.possibleMoves = []
        self.chosenState = None
        self.parent = parent

    def nextMoves(self):
        moves = self.board.nextMoves(self.currentPlayer)
        opponent = Game.otherPlayer(self.currentPlayer)
        states = [State(move, opponent, self.depth - 1, parent=self) for move in moves]

        return states
