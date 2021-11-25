import random
import time

pieceScores = {"K": 0, "Q": 900, "R": 500, "B": 300, "N": 300, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 3
nextMove = None
counter = 0
threatCost = 2
protectionCost = 2

knightPositionScore = [[1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 2, 2, 2, 2, 2, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 2, 3, 4, 4, 3, 2, 1],
                       [1, 2, 3, 4, 4, 3, 2, 1],
                       [1, 2, 3, 3, 3, 3, 2, 1],
                       [1, 2, 2, 2, 2, 2, 2, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1]]
bishopPositionScore = [[2, 2, 2, 1, 1, 2, 2, 2],
                       [2, 4, 3, 3, 3, 3, 4, 2],
                       [2, 3, 3, 3, 3, 3, 3, 2],
                       [2, 3, 3, 3, 3, 3, 3, 2],
                       [2, 3, 3, 3, 3, 3, 3, 2],
                       [2, 3, 3, 3, 3, 3, 3, 2],
                       [2, 4, 3, 3, 3, 3, 4, 2],
                       [2, 2, 2, 1, 1, 2, 2, 2]]
queenPositionScore = [[1, 2, 1, 3, 1, 1, 1, 1],
                      [1, 2, 4, 3, 3, 1, 1, 1],
                      [1, 4, 2, 2, 2, 2, 3, 1],
                      [3, 2, 2, 3, 3, 2, 2, 3],
                      [3, 2, 2, 3, 3, 2, 2, 3],
                      [1, 4, 2, 2, 2, 2, 3, 1],
                      [1, 2, 4, 3, 3, 1, 1, 1],
                      [1, 2, 1, 3, 1, 1, 1, 1]]
rookPositionScore = [[4, 3, 4, 4, 4, 4, 3, 4],
                     [4, 4, 4, 4, 4, 4, 4, 4],
                     [2, 2, 2, 2, 2, 2, 2, 2],
                     [1, 2, 2, 2, 2, 2, 2, 1],
                     [1, 2, 2, 2, 2, 2, 2, 1],
                     [2, 2, 2, 2, 2, 2, 2, 2],
                     [4, 4, 4, 4, 4, 4, 4, 4],
                     [4, 3, 4, 4, 4, 4, 3, 4]]
whitePawnPositionScore = [[4, 4, 4, 4, 4, 4, 4, 4],
                          [4, 4, 4, 4, 4, 4, 4, 4],
                          [4, 4, 4, 4, 4, 4, 4, 4],
                          [3, 3, 4, 4, 4, 4, 3, 3],
                          [2, 2, 3, 3, 3, 3, 2, 2],
                          [2, 2, 3, 3, 3, 3, 2, 2],
                          [1, 1, 1, 1, 0, 1, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0]]
blackPawnPositionScore = [[0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 0, 1, 1, 1],
                          [2, 2, 3, 3, 3, 3, 2, 2],
                          [2, 2, 3, 3, 3, 3, 2, 2],
                          [3, 3, 4, 4, 4, 4, 3, 3],
                          [4, 4, 4, 4, 4, 4, 4, 4],
                          [4, 4, 4, 4, 4, 4, 4, 4],
                          [4, 4, 4, 4, 4, 4, 4, 4]]

piecePositionScores = {"Q": queenPositionScore, "R": rookPositionScore, "B": bishopPositionScore,
                       "N": knightPositionScore, "bp": blackPawnPositionScore, "wp": whitePawnPositionScore}


def randomMoveAI(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def negaMaxWithPruningMoveAI(gameState, validMoves, returnQ):
    global nextMove, counter
    nextMove = None
    # random.shuffle(validMoves)
    # validMoves.sort(key=lambda move: move.isCapture, reverse=True)
    # validMoves.sort(key=lambda move: move.isCastle, reverse=True)
    # print(validMoves)
    counter = 0
    start = time.perf_counter()
    negaMaxWithPruningAI(gameState, validMoves, -CHECKMATE, CHECKMATE, 1 if gameState.whiteTurn else -1)
    print("Thinking time:", time.perf_counter() - start, "s")
    print("Positions calculated:", counter)
    returnQ.put(nextMove)


# def negaMaxWithPruningAI(gameState, validMoves, alpha, beta, turn, depth=DEPTH):
#     global nextMove, counter
#     counter += 1
#     if depth == 0:
#         return turn * scoreBoard(gameState)
#     maxScore = -CHECKMATE
#     # random.shuffle(validMoves)
#     validMoves.sort(key=lambda mov: mov.isCapture, reverse=True)
#     validMoves.sort(key=lambda mov: mov.isCastle, reverse=True)
#     for move in validMoves:
#         gameState.makeMove(move)
#         nextMoves = gameState.getValidMoves()
#         score = -negaMaxWithPruningAI(gameState, nextMoves, -beta, -alpha, -turn, depth - 1)
#         if score > maxScore:
#             maxScore = score
#             if depth == DEPTH:
#                 nextMove = move
#                 print(move, score)
#         gameState.undoMove()
#         if maxScore > alpha:
#             alpha = maxScore
#         if alpha >= beta:
#             break
#     return maxScore


def negaMaxWithPruningAI(gameState, validMoves, alpha, beta, turn, depth=DEPTH):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turn * scoreBoard(gameState)
    # random.shuffle(validMoves)
    validMoves.sort(key=lambda mov: mov.isCapture, reverse=True)
    validMoves.sort(key=lambda mov: mov.isCastle, reverse=True)
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -negaMaxWithPruningAI(gameState, nextMoves, -beta, -alpha, -turn, depth - 1)
        gameState.undoMove()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
    return alpha


def scoreProtectionsAndThreats(gameState):
    moves = gameState.getPossibleMoves(True)
    gameState.whiteTurn = not gameState.whiteTurn
    moves += gameState.getPossibleMoves(True)
    gameState.whiteTurn = not gameState.whiteTurn
    threatsDifference = 0
    protectionsDifference = 0
    for move in moves:
        if not move.isEnpassant:
            if move.capturedPiece[0] == "w" and move.movedPiece[0] == "w":
                protectionsDifference += 1
            elif move.capturedPiece[0] == "b" and move.movedPiece[0] == "b":
                protectionsDifference -= 1
            elif move.capturedPiece[0] == "b" and move.movedPiece[0] == "w":
                threatsDifference += 1
            elif move.capturedPiece[0] == "w" and move.movedPiece[0] == "b":
                threatsDifference -= 1
    return threatsDifference, protectionsDifference


def scoreBoard(gameState):
    if gameState.checkmate:
        if gameState.whiteTurn:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gameState.stalemate:
        return STALEMATE
    threatsDifference, protectionsDifference = scoreProtectionsAndThreats(gameState)
    score = threatsDifference * threatCost + protectionsDifference * protectionCost
    if gameState.isWhiteCastled:
        score += 50
    if gameState.isBlackCastled:
        score -= 50
    if gameState.isWhiteInCheck:
        score -= 20
    if gameState.isBlackInCheck:
        score += 20
    for row in range(len(gameState.board)):
        for column in range(len(gameState.board[row])):
            square = gameState.board[row][column]
            if square != "--":
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][column] * 10
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][column] * 10
                if square[0] == "w":
                    score += pieceScores[square[1]] + piecePositionScore
                elif square[0] == "b":
                    score -= pieceScores[square[1]] + piecePositionScore
    return score
