from Game import Game


def minimax(state):
    if state.depth == 0 or state.board.gameOver():
        state.score = state.board.estimateScore(state.depth)
        return state

    state.possibleMoves = state.nextMoves()
    statesWithScores = [minimax(move) for move in state.possibleMoves]

    if state.currentPlayer == Game.JMAX:
        state.chosenState = max(statesWithScores, key=lambda x: x.score)
    else:
        state.chosenState = min(statesWithScores, key=lambda x: x.score)

    state.score = state.chosenState.score
    return state
