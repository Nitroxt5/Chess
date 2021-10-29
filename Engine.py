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

    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.movedPiece
        self.gameLog.append(move)
        self.whiteTurn = not self.whiteTurn

    def undoMove(self):
        if len(self.gameLog) != 0:
            move = self.gameLog.pop()
            self.board[move.startRow][move.startColumn] = move.movedPiece
            self.board[move.endRow][move.endColumn] = move.capturedPiece
            self.whiteTurn = not self.whiteTurn

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
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Move((column, row), (column + 1, row - 1), self.board))
        if not self.whiteTurn:
            if self.board[row + 1][column] == "--":
                moves.append(Move((column, row), (column, row + 1), self.board))
                if row == 1 and self.board[row + 2][column] == "--":
                    moves.append(Move((column, row), (column, row + 2), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == "w":
                    moves.append(Move((column, row), (column - 1, row + 1), self.board))
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == "w":
                    moves.append(Move((column, row), (column + 1, row + 1), self.board))

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
            if self.board[row - 2][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row - 2), self.board))
        if row - 2 >= 0 and column - 1 >= 0:
            if self.board[row - 2][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row - 2), self.board))
            if self.board[row - 2][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row - 2), self.board))
        if row - 1 >= 0 and column + 2 <= 7:
            if self.board[row - 1][column + 2] == "--":
                moves.append(Move((column, row), (column + 2, row - 1), self.board))
            if self.board[row - 1][column + 2][0] == enemyColor:
                moves.append(Move((column, row), (column + 2, row - 1), self.board))
        if row + 1 <= 7 and column + 2 <= 7:
            if self.board[row + 1][column + 2] == "--":
                moves.append(Move((column, row), (column + 2, row + 1), self.board))
            if self.board[row + 1][column + 2][0] == enemyColor:
                moves.append(Move((column, row), (column + 2, row + 1), self.board))
        if row + 2 <= 7 and column + 1 <= 7:
            if self.board[row + 2][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row + 2), self.board))
            if self.board[row + 2][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row + 2), self.board))
        if row + 2 <= 7 and column - 1 >= 0:
            if self.board[row + 2][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row + 2), self.board))
            if self.board[row + 2][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row + 2), self.board))
        if row + 1 <= 7 and column - 2 >= 0:
            if self.board[row + 1][column - 2] == "--":
                moves.append(Move((column, row), (column - 2, row + 1), self.board))
            if self.board[row + 1][column - 2][0] == enemyColor:
                moves.append(Move((column, row), (column - 2, row + 1), self.board))
        if row - 1 >= 0 and column - 2 >= 0:
            if self.board[row - 1][column - 2] == "--":
                moves.append(Move((column, row), (column - 2, row - 1), self.board))
            if self.board[row - 1][column - 2][0] == enemyColor:
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
            if self.board[row - 1][column][0] == enemyColor:
                moves.append(Move((column, row), (column, row - 1), self.board))
        if row - 1 >= 0 and column + 1 <= 7:
            if self.board[row - 1][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row - 1), self.board))
            if self.board[row - 1][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row - 1), self.board))
        if column + 1 <= 7:
            if self.board[row][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row), self.board))
            if self.board[row][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row), self.board))
        if row + 1 <= 7 and column + 1 <= 7:
            if self.board[row + 1][column + 1] == "--":
                moves.append(Move((column, row), (column + 1, row + 1), self.board))
            if self.board[row + 1][column + 1][0] == enemyColor:
                moves.append(Move((column, row), (column + 1, row + 1), self.board))
        if row + 1 <= 7:
            if self.board[row + 1][column] == "--":
                moves.append(Move((column, row), (column, row + 1), self.board))
            if self.board[row + 1][column][0] == enemyColor:
                moves.append(Move((column, row), (column, row + 1), self.board))
        if row + 1 <= 7 and column - 1 >= 0:
            if self.board[row + 1][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row + 1), self.board))
            if self.board[row + 1][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row + 1), self.board))
        if column - 1 >= 0:
            if self.board[row][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row), self.board))
            if self.board[row][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row), self.board))
        if row - 1 >= 0 and column - 1 >= 0:
            if self.board[row - 1][column - 1] == "--":
                moves.append(Move((column, row), (column - 1, row - 1), self.board))
            if self.board[row - 1][column - 1][0] == enemyColor:
                moves.append(Move((column, row), (column - 1, row - 1), self.board))

    def getValidMoves(self):
        return self.getPossibleMoves()


class Move:
    rowToNumber = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
    columnToLetter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    numberToRow = {v: k for k, v in rowToNumber.items()}
    letterToColumn = {v: k for k, v in columnToLetter.items()}

    def __init__(self, startSq, endSq, board):
        self.startColumn = startSq[0]
        self.startRow = startSq[1]
        self.endColumn = endSq[0]
        self.endRow = endSq[1]
        self.movedPiece = board[self.startRow][self.startColumn]
        self.capturedPiece = board[self.endRow][self.endColumn]
        self.moveID = self.startColumn * 1000 + self.startRow * 100 + self.endColumn * 10 + self.endRow

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getSquareNotation(self, row, column):
        return self.columnToLetter[column] + self.rowToNumber[row]

    def getMoveNotation(self):
        return self.getSquareNotation(self.startRow, self.startColumn) + " - " + self.getSquareNotation(self.endRow,
                                                                                                        self.endColumn)
