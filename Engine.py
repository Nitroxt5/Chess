class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunc = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                         "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteTurn = True
        self.gameLog = []
        self.whiteKingPos = (4, 7)
        self.blackKingPos = (4, 0)
        self.checkmate = False
        self.stalemate = False
        self.enpassantSq = ()
        self.enpassantSqLog = [self.enpassantSq]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wKs, self.currentCastlingRight.wQs,
                                             self.currentCastlingRight.bKs, self.currentCastlingRight.bQs)]
        self.isWhiteCastled = False
        self.isBlackCastled = False
        self.isWhiteInCheck = False
        self.isBlackInCheck = False

    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.movedPiece
        self.gameLog.append(move)
        if move.movedPiece == "wK":
            self.whiteKingPos = (move.endColumn, move.endRow)
        elif move.movedPiece == "bK":
            self.blackKingPos = (move.endColumn, move.endRow)
        if move.isPawnPromotion:
            self.board[move.endRow][move.endColumn] = move.movedPiece[0] + "Q"
        if move.isEnpassant:
            self.board[move.startRow][move.endColumn] = "--"
        if move.movedPiece[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassantSq = (move.startColumn, (move.startRow + move.endRow) // 2)
        else:
            self.enpassantSq = ()
        self.enpassantSqLog.append(self.enpassantSq)
        if move.isCastle:
            if move.endColumn - move.startColumn == 2:
                self.board[move.endRow][move.endColumn - 1] = self.board[move.endRow][move.endColumn + 1]
                self.board[move.endRow][move.endColumn + 1] = "--"
            else:
                self.board[move.endRow][move.endColumn + 1] = self.board[move.endRow][move.endColumn - 2]
                self.board[move.endRow][move.endColumn - 2] = "--"
            if move.startRow == 7:
                self.isWhiteCastled = True
            else:
                self.isBlackCastled = True
        self.inCheck()
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wKs, self.currentCastlingRight.wQs,
                                                 self.currentCastlingRight.bKs, self.currentCastlingRight.bQs))
        self.whiteTurn = not self.whiteTurn

    def undoMove(self):
        if len(self.gameLog) != 0:
            move = self.gameLog.pop()
            self.board[move.startRow][move.startColumn] = move.movedPiece
            self.board[move.endRow][move.endColumn] = move.capturedPiece
            if move.movedPiece == "wK":
                self.whiteKingPos = (move.startColumn, move.startRow)
            elif move.movedPiece == "bK":
                self.blackKingPos = (move.startColumn, move.startRow)
            if move.isEnpassant:
                self.board[move.endRow][move.endColumn] = "--"
                self.board[move.startRow][move.endColumn] = move.capturedPiece
            self.enpassantSqLog.pop()
            self.enpassantSq = self.enpassantSqLog[-1]
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wKs, newRights.wQs, newRights.bKs, newRights.bQs)
            if move.isCastle:
                if move.endColumn - move.startColumn == 2:
                    self.board[move.endRow][move.endColumn + 1] = self.board[move.endRow][move.endColumn - 1]
                    self.board[move.endRow][move.endColumn - 1] = "--"
                else:
                    self.board[move.endRow][move.endColumn - 2] = self.board[move.endRow][move.endColumn + 1]
                    self.board[move.endRow][move.endColumn + 1] = "--"
                if move.startRow == 7:
                    self.isWhiteCastled = False
                else:
                    self.isBlackCastled = False
            self.checkmate = False
            self.stalemate = False
            self.whiteTurn = not self.whiteTurn

    def updateCastleRights(self, move):
        if move.movedPiece == "wK":
            self.currentCastlingRight.wKs = False
            self.currentCastlingRight.wQs = False
        elif move.movedPiece == "bK":
            self.currentCastlingRight.bKs = False
            self.currentCastlingRight.bQs = False
        elif move.movedPiece == "wR":
            if move.startRow == 7:
                if move.startColumn == 0:
                    self.currentCastlingRight.wQs = False
                elif move.startColumn == 7:
                    self.currentCastlingRight.wKs = False
        elif move.movedPiece == "bR":
            if move.startRow == 0:
                if move.startColumn == 0:
                    self.currentCastlingRight.bQs = False
                elif move.startColumn == 7:
                    self.currentCastlingRight.bKs = False
        if move.capturedPiece == "wR":
            if move.endRow == 7:
                if move.endColumn == 0:
                    self.currentCastlingRight.wQs = False
                elif move.endColumn == 7:
                    self.currentCastlingRight.wKs = False
        elif move.capturedPiece == "bR":
            if move.endRow == 0:
                if move.endColumn == 0:
                    self.currentCastlingRight.bQs = False
                elif move.endColumn == 7:
                    self.currentCastlingRight.bKs = False

    def getPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == "w" and self.whiteTurn) or (turn == "b" and not self.whiteTurn):
                    piece = self.board[row][column][1]
                    self.moveFunc[piece](row, column, moves)
        return moves

    def getPawnMoves(self, row, column, moves):
        if self.whiteTurn:
            if self.board[row - 1][column] == "--":
                moves.append(Move((column, row), (column, row - 1), self.board))
                if row == 6 and self.board[row - 2][column] == "--":
                    moves.append(Move((column, row), (column, row - 2), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(Move((column, row), (column - 1, row - 1), self.board))
                elif (column - 1, row - 1) == self.enpassantSq:
                    moves.append(Move((column, row), (column - 1, row - 1), self.board, isEnpassant=True))
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Move((column, row), (column + 1, row - 1), self.board))
                elif (column + 1, row - 1) == self.enpassantSq:
                    moves.append(Move((column, row), (column + 1, row - 1), self.board, isEnpassant=True))
        if not self.whiteTurn:
            if self.board[row + 1][column] == "--":
                moves.append(Move((column, row), (column, row + 1), self.board))
                if row == 1 and self.board[row + 2][column] == "--":
                    moves.append(Move((column, row), (column, row + 2), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == "w":
                    moves.append(Move((column, row), (column - 1, row + 1), self.board))
                elif (column - 1, row + 1) == self.enpassantSq:
                    moves.append(Move((column, row), (column - 1, row + 1), self.board, isEnpassant=True))
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == "w":
                    moves.append(Move((column, row), (column + 1, row + 1), self.board))
                elif (column + 1, row + 1) == self.enpassantSq:
                    moves.append(Move((column, row), (column + 1, row + 1), self.board, isEnpassant=True))

    def getRookMoves(self, row, column, moves):
        enemyColor = "b" if self.whiteTurn else "w"
        checkingRow = row
        while checkingRow > 0:
            checkingRow -= 1
            if self.board[checkingRow][column] == "--":
                moves.append(Move((column, row), (column, checkingRow), self.board))
            elif self.board[checkingRow][column][0] == enemyColor:
                moves.append(Move((column, row), (column, checkingRow), self.board))
                break
            else:
                break
        checkingRow = row
        while checkingRow < 7:
            checkingRow += 1
            if self.board[checkingRow][column] == "--":
                moves.append(Move((column, row), (column, checkingRow), self.board))
            elif self.board[checkingRow][column][0] == enemyColor:
                moves.append(Move((column, row), (column, checkingRow), self.board))
                break
            else:
                break
        checkingColumn = column
        while checkingColumn > 0:
            checkingColumn -= 1
            if self.board[row][checkingColumn] == "--":
                moves.append(Move((column, row), (checkingColumn, row), self.board))
            elif self.board[row][checkingColumn][0] == enemyColor:
                moves.append(Move((column, row), (checkingColumn, row), self.board))
                break
            else:
                break
        checkingColumn = column
        while checkingColumn < 7:
            checkingColumn += 1
            if self.board[row][checkingColumn] == "--":
                moves.append(Move((column, row), (checkingColumn, row), self.board))
            elif self.board[row][checkingColumn][0] == enemyColor:
                moves.append(Move((column, row), (checkingColumn, row), self.board))
                break
            else:
                break

    def getKnightMoves(self, row, column, moves):
        enemyColor = "b" if self.whiteTurn else "w"
        if row - 2 >= 0 and column + 1 <= 7:
            if self.board[row - 2][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row - 2), self.board))
            elif self.board[row - 2][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row - 2), self.board))
        if row - 2 >= 0 and column - 1 >= 0:
            if self.board[row - 2][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row - 2), self.board))
            elif self.board[row - 2][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row - 2), self.board))
        if row - 1 >= 0 and column + 2 <= 7:
            if self.board[row - 1][column + 2] == "--":
                moves.append(Move((column, row), (column + 2, row - 1), self.board))
            elif self.board[row - 1][column + 2][0] == enemyColor:
                moves.append(Move((column, row), (column + 2, row - 1), self.board))
        if row + 1 <= 7 and column + 2 <= 7:
            if self.board[row + 1][column + 2] == "--":
                moves.append(Move((column, row), (column + 2, row + 1), self.board))
            elif self.board[row + 1][column + 2][0] == enemyColor:
                moves.append(Move((column, row), (column + 2, row + 1), self.board))
        if row + 2 <= 7 and column + 1 <= 7:
            if self.board[row + 2][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row + 2), self.board))
            elif self.board[row + 2][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row + 2), self.board))
        if row + 2 <= 7 and column - 1 >= 0:
            if self.board[row + 2][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row + 2), self.board))
            elif self.board[row + 2][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row + 2), self.board))
        if row + 1 <= 7 and column - 2 >= 0:
            if self.board[row + 1][column - 2] == "--":
                moves.append(Move((column, row), (column - 2, row + 1), self.board))
            elif self.board[row + 1][column - 2][0] == enemyColor:
                moves.append(Move((column, row), (column - 2, row + 1), self.board))
        if row - 1 >= 0 and column - 2 >= 0:
            if self.board[row - 1][column - 2] == "--":
                moves.append(Move((column, row), (column - 2, row - 1), self.board))
            elif self.board[row - 1][column - 2][0] == enemyColor:
                moves.append(Move((column, row), (column - 2, row - 1), self.board))

    def getBishopMoves(self, row, column, moves):
        enemyColor = "b" if self.whiteTurn else "w"
        checkingRow = row
        checkingColumn = column
        while checkingRow > 0 and checkingColumn < 7:
            checkingRow -= 1
            checkingColumn += 1
            if self.board[checkingRow][checkingColumn] == "--":
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
            elif self.board[checkingRow][checkingColumn][0] == enemyColor:
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
                break
            else:
                break
        checkingRow = row
        checkingColumn = column
        while checkingRow > 0 and checkingColumn > 0:
            checkingRow -= 1
            checkingColumn -= 1
            if self.board[checkingRow][checkingColumn] == "--":
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
            elif self.board[checkingRow][checkingColumn][0] == enemyColor:
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
                break
            else:
                break
        checkingRow = row
        checkingColumn = column
        while checkingRow < 7 and checkingColumn < 7:
            checkingRow += 1
            checkingColumn += 1
            if self.board[checkingRow][checkingColumn] == "--":
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
            elif self.board[checkingRow][checkingColumn][0] == enemyColor:
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
                break
            else:
                break
        checkingRow = row
        checkingColumn = column
        while checkingRow < 7 and checkingColumn > 0:
            checkingRow += 1
            checkingColumn -= 1
            if self.board[checkingRow][checkingColumn] == "--":
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
            elif self.board[checkingRow][checkingColumn][0] == enemyColor:
                moves.append(Move((column, row), (checkingColumn, checkingRow), self.board))
                break
            else:
                break

    def getQueenMoves(self, row, column, moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column, moves):
        enemyColor = "b" if self.whiteTurn else "w"
        if row - 1 >= 0:
            if self.board[row - 1][column] == "--":
                moves.append(Move((column, row), (column, row - 1), self.board))
            elif self.board[row - 1][column][0] == enemyColor:
                moves.append(Move((column, row), (column, row - 1), self.board))
        if row - 1 >= 0 and column + 1 <= 7:
            if self.board[row - 1][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row - 1), self.board))
            elif self.board[row - 1][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row - 1), self.board))
        if column + 1 <= 7:
            if self.board[row][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row), self.board))
            elif self.board[row][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row), self.board))
        if row + 1 <= 7 and column + 1 <= 7:
            if self.board[row + 1][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row + 1), self.board))
            elif self.board[row + 1][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row + 1), self.board))
        if row + 1 <= 7:
            if self.board[row + 1][column] == "--":
                moves.append(Move((column, row), (column, row + 1), self.board))
            elif self.board[row + 1][column][0] == enemyColor:
                moves.append(Move((column, row), (column, row + 1), self.board))
        if row + 1 <= 7 and column - 1 >= 0:
            if self.board[row + 1][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row + 1), self.board))
            elif self.board[row + 1][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row + 1), self.board))
        if column - 1 >= 0:
            if self.board[row][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row), self.board))
            elif self.board[row][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row), self.board))
        if row - 1 >= 0 and column - 1 >= 0:
            if self.board[row - 1][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row - 1), self.board))
            elif self.board[row - 1][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row - 1), self.board))

    def getCastleMoves(self, row, column, moves):
        if self.isSquareAttacked(row, column):
            return
        if (self.whiteTurn and self.currentCastlingRight.wKs) or (not self.whiteTurn and self.currentCastlingRight.bKs):
            self.getKingSideCastle(row, column, moves)
        if (self.whiteTurn and self.currentCastlingRight.wQs) or (not self.whiteTurn and self.currentCastlingRight.bQs):
            self.getQueenSideCastle(row, column, moves)

    def getKingSideCastle(self, row, column, moves):
        if self.board[row][column + 1] == "--" and self.board[row][column + 2] == "--":
            if not self.isSquareAttacked(row, column + 1) and not self.isSquareAttacked(row, column + 2):
                moves.append(Move((column, row), (column + 2, row), self.board, isCastle=True))

    def getQueenSideCastle(self, row, col, moves):
        if self.board[row][col - 1] == "--" and self.board[row][col - 2] == "--" and self.board[row][col - 3] == "--":
            if not self.isSquareAttacked(row, col - 1) and not self.isSquareAttacked(row, col - 2):
                moves.append(Move((col, row), (col - 2, row), self.board, isCastle=True))

    def getValidMoves(self):
        enpassantSq = self.enpassantSq
        currentCastlingRight = CastleRights(self.currentCastlingRight.wKs, self.currentCastlingRight.wQs,
                                            self.currentCastlingRight.bKs, self.currentCastlingRight.bQs)
        moves = self.getPossibleMoves()
        if self.whiteTurn:
            self.getCastleMoves(self.whiteKingPos[1], self.whiteKingPos[0], moves)
        else:
            self.getCastleMoves(self.blackKingPos[1], self.blackKingPos[0], moves)
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteTurn = not self.whiteTurn
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteTurn = not self.whiteTurn
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.enpassantSq = enpassantSq
        self.currentCastlingRight = currentCastlingRight
        return moves

    def inCheck(self):
        if self.whiteTurn:
            self.isWhiteInCheck = self.isSquareAttacked(self.whiteKingPos[1], self.whiteKingPos[0])
            return self.isWhiteInCheck
        else:
            self.isBlackInCheck = self.isSquareAttacked(self.blackKingPos[1], self.blackKingPos[0])
            return self.isBlackInCheck

    def isSquareAttacked(self, row, column):
        self.whiteTurn = not self.whiteTurn
        opponentMoves = self.getPossibleMoves()
        self.whiteTurn = not self.whiteTurn
        for move in opponentMoves:
            if move.endRow == row and move.endColumn == column:
                return True
        return False


class CastleRights:
    def __init__(self, wKs, wQs, bKs, bQs):
        self.wKs = wKs
        self.wQs = wQs
        self.bKs = bKs
        self.bQs = bQs


class Move:
    rowToNumber = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
    columnToLetter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    numberToRow = {v: k for k, v in rowToNumber.items()}
    letterToColumn = {v: k for k, v in columnToLetter.items()}

    def __init__(self, startSq, endSq, board, isEnpassant=False, isCastle=False):
        self.startColumn = startSq[0]
        self.startRow = startSq[1]
        self.endColumn = endSq[0]
        self.endRow = endSq[1]
        self.movedPiece = board[self.startRow][self.startColumn]
        self.capturedPiece = board[self.endRow][self.endColumn]
        self.moveID = self.startColumn * 1000 + self.startRow * 100 + self.endColumn * 10 + self.endRow
        self.isPawnPromotion = (self.movedPiece == "wp" and self.endRow == 0) or (
                self.movedPiece == "bp" and self.endRow == 7)
        self.isEnpassant = isEnpassant
        if self.isEnpassant:
            self.capturedPiece = "bp" if self.movedPiece == "wp" else "wp"
        self.isCastle = isCastle

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __repr__(self):
        return self.getMoveNotation()

    def __str__(self):
        return self.getMoveNotation()

    def getSquareNotation(self, row, column):
        return self.columnToLetter[column] + self.rowToNumber[row]

    def getMoveNotation(self):
        if self.isCastle:
            if self.endColumn == 6:
                return "0-0"
            elif self.endColumn == 2:
                return "0-0-0"
        moveNotation = ""
        if self.movedPiece[1] != "p":
            moveNotation = self.movedPiece[1]
        moveNotation += self.getSquareNotation(self.startRow, self.startColumn)
        if self.capturedPiece != "--":
            moveNotation += "x"
        else:
            moveNotation += "-"
        moveNotation += self.getSquareNotation(self.endRow, self.endColumn)
        return moveNotation
