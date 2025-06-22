import random

piecescore = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
Checkmate = 1000
staleMate = 0
depth = 2
nextmove = None  # Define it once at global scope


def findrandommove(validmoves):
    if len(validmoves) == 0:
        return None
    return validmoves[random.randint(0, len(validmoves) - 1)]


def findbestmethod(gs, validmove):
    turnMultiplier = 1 if gs.whitetomove else -1
    opponentMinMaxscore = Checkmate
    bestplayermove = None
    random.shuffle(validmove)
    for playermove in validmove:
        gs.makemove(playermove)
        opponentMoves = gs.getvalidmove()
        opponentmaxscore = -Checkmate
        if gs.checkmate:
            opponentmaxscore = -turnMultiplier * Checkmate
        elif gs.Stalemate:
            opponentmaxscore = staleMate
        else:
            for opponentmove in opponentMoves:
                gs.makemove(opponentmove)
                if gs.checkmate:
                    score = Checkmate
                elif gs.Stalemate:
                    score = staleMate
                else:
                    score = -turnMultiplier * scorematerial(gs.board)
                if score > opponentmaxscore:
                    opponentmaxscore = score
                gs.undomove()
        if opponentmaxscore < opponentMinMaxscore:
            opponentMinMaxscore = opponentmaxscore
            bestplayermove = playermove
        gs.undomove()
        gs.checkmate=False
        gs.stalemete=False

    return bestplayermove


def findbestmoveminmax(gs, valid):
    global nextmove
    nextmove = None  # reset before every new call
    findmoveminmax(gs, valid, depth, gs.whitetomove)
    return nextmove


def findmoveminmax(gs, validMoves, depth, whitetomove):
    global nextmove
    if depth == 0:
        return ScoreBoard(gs)

    if whitetomove:
        maxScore = -Checkmate
        bestMove = None
        for move in validMoves:
            gs.makemove(move)
            nextValidMoves = gs.getvalidmove()
            score = findmoveminmax(gs, nextValidMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                bestMove = move
            gs.undomove()
        if depth == 2:  # only set at root depth
            nextmove = bestMove
        return maxScore

    else:
        minScore = Checkmate
        bestMove = None
        for move in validMoves:
            gs.makemove(move)
            nextValidMoves = gs.getvalidmove()
            score = findmoveminmax(gs, nextValidMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                bestMove = move
            gs.undomove()
        if depth == 2:
            nextmove = bestMove
        return minScore


def ScoreBoard(gs):
    if gs.checkmate:
        if gs.whitetomove:
            return -Checkmate
        else:
            return Checkmate
    elif gs.Stalemate:
        return staleMate
    score = 0
    for row in gs.board:
        for sqare in row:
            if sqare[0] == 'w':
                score += piecescore[sqare[1]]
            elif sqare[0] == 'b':
                score -= piecescore[sqare[1]]
    return score


def scorematerial(board):
    score = 0
    for row in board:
        for sqare in row:
            if sqare[0] == 'w':
                score += piecescore[sqare[1]]
            elif sqare[0] == 'b':
                score -= piecescore[sqare[1]]
    return score
  