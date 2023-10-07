from Game import Game
from State import State
from random import randint
import copy

noOfNodes = 0


def updateExtremeTiles(state):
    i = 0
    j = 0
    ok = False
    # cautam prima pozitie in care a mutat calculatorul
    # pentru a actualiza piesa extrema
    for i in range(state.chosenState.board.NUM_ROWS):
        for j in range(state.chosenState.board.NUM_COLS):
            if state.chosenState.board.matrix[i][j] == state.board.JMAX[0].upper():
                ok = True
                break
        if ok:
            break

    # newPos = (coordonata pe x, coordonata pe y) = (coloana, linia)
    newPos = (j, i)
    # daca JMAX joaca cu rosu, atunci actualizam fie cea mai de sus piesa, fie cea mai de jos
    if state.board.JMAX == 'red':
        # verificam existenta celei mai de sus piese rosii
        if Game.topTile is None:
            Game.topTile = newPos
        else:
            # o actualizam daca a mutat mai sus de ea
            if i < Game.topTile[1]:
                Game.topTile = newPos

        # verificam existenta celei mai de jos piese rosii
        if Game.bottomTile is None:
            Game.bottomTile = newPos
        else:
            # o actualizam daca a mutat mai jos de ea
            if i > Game.bottomTile[1]:
                Game.bottomTile = newPos

    # altfel, daca JMAX joaca cu albastru, actualizam cea mai din stanga / dreapta piesa
    elif state.board.JMAX == 'blue':
        # verificam existenta celei mai din stanga piese albastre
        if Game.leftTile is None:
            Game.leftTile = newPos
        else:
            # o actualizam daca a mutat mai in stanga de ea
            if j < Game.leftTile[0]:
                Game.leftTile = newPos

        # verificam existenta celei mai din dreapta piese rosii
        if Game.rightTile is None:
            Game.rightTile = newPos
        else:
            # o actualizam daca a mutat mai in dreapta de ea
            if j > Game.rightTile[0]:
                Game.rightTile = newPos


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
    global noOfNodes

    # am ajuns la limita adancimii in arbore SAU la o stare finala
    if state.depth == 0 or state.board.gameOver():
        # estimam scorul pentru starea
        state.score = state.board.estimateScore(state.depth)
        return state

    # generam fiii nodului curent (urmatoarele mutari posibile)
    state.possibleMoves = state.nextMoves()

    # daca este prima mutare, atunci calculatorul muta random
    createPossibleMove(state)

    # mergem recursiv in fiii starii curente
    statesWithScores = [minimax(move) for move in state.possibleMoves]
    noOfNodes += len(statesWithScores)

    # daca suntem in arbore pe un nivel MAX (e randul calculatorului)
    if state.currentPlayer == Game.JMAX:
        # atunci alegem maximul dintre mutarile fii (raportat la f)
        state.chosenState = max(statesWithScores, key=lambda x: x.score)
    else:
        # altfel, suntem pe mutarea jucatorului, deci alegem minimul dintre fii (raportat la f)
        state.chosenState = min(statesWithScores, key=lambda x: x.score)

    # actualizam piesele din pozitii extreme
    updateExtremeTiles(state)

    # dupa ce am ales urmatoarea mutare cea mai buna pentru calculator,
    # actualizam scorul starii curente
    # => actualizarea bottom-up a arborelui
    state.score = state.chosenState.score
    return state


def alpha_beta(alpha, beta, state):
    global noOfNodes

    # daca am ajuns la ultimul nivel al arborelui SAU am ajuns intr-o stare castigatoare
    if state.depth == 0 or state.board.gameOver():
        # calculam scorul starii
        state.score = state.board.estimateScore(state.depth)
        return state

    # interval invalid, oprim cautarea
    if alpha > beta:
        return state

    # generam urmatoarele mutari posibile
    state.possibleMoves = state.nextMoves()

    # daca este prima mutare, calculatorul pune random o piesa pe tabla
    createPossibleMove(state)

    # daca jucatorul curent este MAX (calculatorul)
    if state.currentPlayer == Game.JMAX:

        # scorul initial maxim este -infinit
        currentScore = float('-inf')

        # mergem recursiv in urmatoarele stari posibile
        for move in state.possibleMoves:
            newState = alpha_beta(alpha, beta, move)
            noOfNodes += 1

            # calculam valoarea maxima dintre fiii nodului curent
            # si actualizam starea aleasa
            if currentScore < newState.score:
                state.chosenState = newState
                currentScore = newState.score

            # verificam daca valoarea fiului poate maximiza alpha pentru tata
            if alpha < newState.score:
                alpha = newState.score
                # daca am actualizat alpha si am ajuns la un interval invalid, ne oprim
                if alpha >= beta:
                    break

    # daca jucatorul curent este MIN (jucatorul)
    elif state.currentPlayer == Game.JMIN:

        # scorul initial minim este infinit
        currentScore = float('inf')

        # mergem recursiv in urmatoarele stari posibile
        for move in state.possibleMoves:
            newState = alpha_beta(alpha, beta, move)
            noOfNodes += 1

            # calculam valoarea minima dintre fiii nodului curent
            # si actualizam starea aleasa
            if currentScore > newState.score:
                state.chosenState = newState
                currentScore = newState.score

            # verificam daca valoarea fiului poate minimiza beta pentru tata
            if beta > newState.score:
                beta = newState.score
                # daca am actualizat beta si am ajuns la un interval invalid, ne oprim
                if alpha >= beta:
                    break

    # actualizam piesele din pozitii extreme
    updateExtremeTiles(state)

    # dupa ce am ales urmatoarea mutare a jucatorului care sa fie cea mai avantajoasa pentru calculator,
    # actualizam scorul starii curente
    # => actualizarea bottom-up a arborelui
    state.score = state.chosenState.score
    return state
