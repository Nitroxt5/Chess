import random

pieceScores = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2
nextMove = None


def randomMoveAI(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


# Жадный алгоритм (глубина 1)
def greedyMoveAI(gameState, validMoves):
    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in validMoves:
        gameState.makeMove(playerMove)
        if gameState.checkmate:
            score = CHECKMATE
        elif gameState.stalemate:
            score = STALEMATE
        else:
            score = abs(scoreBoard(gameState))
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gameState.undoMove()
    return bestMove


# Жадный алгоритм с применением нерекурсиного минимакса (глубина 2)
def greedyMinMaxMoveAI(gameState, validMoves):
    opponentMinMaxScore = CHECKMATE + 1
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gameState.makeMove(playerMove)
        opponentsMoves = gameState.getValidMoves()
        if gameState.checkmate:
            bestPlayerMove = playerMove
            gameState.undoMove()
            break
        elif gameState.stalemate:
            opponentsMaxScore = STALEMATE
        else:
            opponentsMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            gameState.makeMove(opponentsMove)
            gameState.getValidMoves()
            if gameState.checkmate:
                score = CHECKMATE
            elif gameState.stalemate:
                score = STALEMATE
            else:
                score = abs(scoreBoard(gameState))
            if score > opponentsMaxScore:
                opponentsMaxScore = score
            gameState.undoMove()
        if opponentsMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gameState.undoMove()
    return bestPlayerMove


# Рекурсивный минимакс с настраиваемой глубиной, но больше 2 лучше не ставить
def minMaxMoveAI(gameState, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    minMaxAI(gameState, validMoves, gameState.whiteTurn)
    return nextMove


def minMaxAI(gameState, validMoves, whiteTurn, depth=DEPTH):
    global nextMove
    if depth == 0:
        return scoreBoard(gameState)
    if whiteTurn:
        maxScore = -CHECKMATE
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = minMaxAI(gameState, nextMoves, False, depth - 1)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = minMaxAI(gameState, nextMoves, True, depth - 1)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return minScore


# Алгоритм negamax с настраиваемой глубиной (то же, что и минимакс)
def negaMaxMoveAI(gameState, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    negaMaxAI(gameState, validMoves, 1 if gameState.whiteTurn else -1)
    return nextMove


def negaMaxAI(gameState, validMoves, turn, depth=DEPTH):
    global nextMove
    if depth == 0:
        return turn * scoreBoard(gameState)
    maxScore = -CHECKMATE
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -negaMaxAI(gameState, nextMoves, -turn, depth - 1)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gameState.undoMove()
    return maxScore


def negaMaxWithPruningMoveAI(gameState, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    negaMaxWithPruningAI(gameState, validMoves, -CHECKMATE, CHECKMATE, 1 if gameState.whiteTurn else -1)
    return nextMove


def negaMaxWithPruningAI(gameState, validMoves, alpha, beta, turn, depth=DEPTH):
    global nextMove
    if depth == 0:
        return turn * scoreBoard(gameState)
    maxScore = -CHECKMATE
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -negaMaxWithPruningAI(gameState, nextMoves, -beta, -alpha, -turn, depth - 1)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gameState.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gameState):
    if gameState.checkmate:
        if gameState.whiteTurn:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gameState.stalemate:
        return STALEMATE
    score = 0
    for row in gameState.board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] == "b":
                score -= pieceScores[square[1]]
    return score
