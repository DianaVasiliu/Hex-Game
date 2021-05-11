from Game import Game
from State import State
from random import randint
import copy


def createPossibleMove(state):
    if not state.possibleMoves:
        i = randint(0, state.board.NUM_ROWS - 1)
        j = randint(0, state.board.NUM_COLS - 1)

        newMatrix = copy.deepcopy(state.board.matrix)
        newMatrix[i][j] = state.board.JMAX[0].upper()
        newGame = Game(newMatrix)
        newGame.currentPlayer = state.board.otherPlayer(state.currentPlayer)
        newGame.text = newGame.currentPlayer.capitalize() + '\'s turn'
        move = newGame

        state.possibleMoves.append(State(move, newGame.currentPlayer, state.depth - 1, parent=state))


def minimax(state):
    if state.depth == 0 or state.board.gameOver():
        state.score = state.board.estimateScore(state.depth)
        return state

    state.possibleMoves = state.nextMoves()

    createPossibleMove(state)

    statesWithScores = [minimax(move) for move in state.possibleMoves]

    if state.currentPlayer == Game.JMAX:
        state.chosenState = max(statesWithScores, key=lambda x: x.score)
    else:
        state.chosenState = min(statesWithScores, key=lambda x: x.score)

    i = 0
    j = 0
    ok = False
    for i in range(state.chosenState.board.NUM_ROWS):
        for j in range(state.chosenState.board.NUM_COLS):
            if state.chosenState.board.matrix[i][j] == state.board.JMAX[0].upper():
                ok = True
                break
        if ok:
            break

    newPos = (j, i)
    if state.board.JMAX == 'red':
        if Game.topTile is None:
            Game.topTile = newPos
        else:
            if i < Game.topTile[1]:
                Game.topTile = newPos

        if Game.bottomTile is None:
            Game.bottomTile = newPos
        else:
            if i > Game.bottomTile[1]:
                Game.bottomTile = newPos
    elif state.board.JMAX == 'blue':
        if Game.leftTile is None:
            Game.leftTile = newPos
        else:
            if j < Game.leftTile[0]:
                Game.leftTile = newPos

        if Game.rightTile is None:
            Game.rightTile = newPos
        else:
            if j > Game.rightTile[0]:
                Game.rightTile = newPos

    state.score = state.chosenState.score
    return state


def alpha_beta(alpha, beta, state):
    if state.depth == 0 or state.board.gameOver():
        state.score = state.board.estimateScore(state.depth)
        return state

    # invalid interval, so we stop processing it
    if alpha > beta:
        return state

    state.possibleMoves = state.nextMoves()

    createPossibleMove(state)

    if state.currentPlayer == Game.JMAX:
        currentScore = float('-inf')

        for move in state.possibleMoves:
            # calculating the score
            newState = alpha_beta(alpha, beta, move)

            if currentScore < newState.score:
                state.chosenState = newState
                currentScore = newState.score
            if alpha < newState.score:
                alpha = newState.score
                if alpha >= beta:
                    break

    elif state.currentPlayer == Game.JMIN:
        currentScore = float('inf')

        for move in state.possibleMoves:

            newState = alpha_beta(alpha, beta, move)

            if currentScore > newState.score:
                state.chosenState = newState
                currentScore = newState.score

            if beta > newState.score:
                beta = newState.score
                if alpha >= beta:
                    break
    state.score = state.chosenState.score
    return state
