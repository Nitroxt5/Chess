import Engine
import pygame
import AI
from multiprocessing import Process, Queue

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {}
COLORS = [pygame.Color("white"), pygame.Color("dark gray")]


def loadImages():
    pieces = ["icon", "wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color("white"))
    gameState = Engine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    gameOver = False
    whitePlayer = True
    blackPlayer = False
    playerColor = False if blackPlayer and not whitePlayer else True
    AIThinking = False
    AIProcess = None

    loadImages()
    pygame.display.set_caption("SwiChess")
    pygame.display.set_icon(IMAGES["icon"])
    selectedSq = ()
    clicks = []

    # working = True
    while True:
        # pygame.time.wait(500)
        playerTurn = (gameState.whiteTurn and whitePlayer) or (not gameState.whiteTurn and blackPlayer)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # working = False
                quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = pygame.mouse.get_pos()
                    column = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if not playerColor:
                        column = DIMENSION - column - 1
                        row = DIMENSION - row - 1
                    if selectedSq == (column, row) or column < 0 or column > 7 or row < 0 or column > 7:
                        selectedSq = ()
                        clicks = []
                    else:
                        selectedSq = (column, row)
                        clicks.append(selectedSq)
                    if len(clicks) == 2 and playerTurn:
                        move = Engine.Move(clicks[0], clicks[1], gameState.board)
                        # print(move.getMoveNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                selectedSq = ()
                                clicks = []
                                break
                        if not moveMade:
                            clicks = [selectedSq]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_u:
                    gameState.undoMove()
                    moveMade = True
                    if gameOver:
                        playerTurn = not playerTurn
                        gameOver = False
                    if AIThinking:
                        AIProcess.terminate()
                        AIThinking = False
                if e.key == pygame.K_r:
                    gameState = Engine.GameState()
                    validMoves = gameState.getValidMoves()
                    selectedSq = ()
                    clicks = []
                    if gameOver:
                        playerTurn = not playerTurn
                        gameOver = False
                    moveMade = False
                    if AIThinking:
                        AIProcess.terminate()
                        AIThinking = False
        if not gameOver and not playerTurn:
            if not AIThinking:
                print("thinking...")
                AIThinking = True
                returnQ = Queue()
                AIProcess = Process(target=AI.negaMaxWithPruningMoveAI, args=(gameState, validMoves, returnQ))
                AIProcess.start()
            if not AIProcess.is_alive():
                AIMove = returnQ.get()
                print("came up with a move")
                if AIMove is None:
                    AIMove = AI.randomMoveAI(validMoves)
                gameState.makeMove(AIMove)
                moveMade = True
                AIThinking = False
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        drawGameState(screen, gameState, validMoves, selectedSq, playerColor)
        if gameState.checkmate:
            gameOver = True
            if gameState.whiteTurn:
                drawEndGameText(screen, "Black win by checkmate")
            else:
                drawEndGameText(screen, "White win by checkmate")
        elif gameState.stalemate:
            gameOver = True
            drawEndGameText(screen, "Stalemate")
        pygame.display.flip()


def highlightSq(screen, gameState, validMoves, selectedSq, playerColor):
    if selectedSq != ():
        column, row = selectedSq
        if gameState.board[row][column][0] == ("w" if gameState.whiteTurn else "b"):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.fill(pygame.Color(110, 90, 0))
            if playerColor:
                screen.blit(s, (column * SQ_SIZE, row * SQ_SIZE))
            else:
                screen.blit(s, ((DIMENSION - 1 - column) * SQ_SIZE, (DIMENSION - 1 - row) * SQ_SIZE))
            s.set_alpha(100)
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.startColumn == column and move.startRow == row:
                    if playerColor:
                        screen.blit(s, (move.endColumn * SQ_SIZE, move.endRow * SQ_SIZE))
                    else:
                        r = DIMENSION - 1 - move.endRow
                        c = DIMENSION - 1 - move.endColumn
                        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def highlightLastMove(screen, gameState, playerColor):
    if len(gameState.gameLog) != 0:
        lastMove = gameState.gameLog[-1]
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(pygame.Color(182, 255, 0))
        if playerColor:
            screen.blit(s, (lastMove.startColumn * SQ_SIZE, lastMove.startRow * SQ_SIZE))
            screen.blit(s, (lastMove.endColumn * SQ_SIZE, lastMove.endRow * SQ_SIZE))
        else:
            screen.blit(s, ((DIMENSION - 1 - lastMove.startColumn) * SQ_SIZE,
                            (DIMENSION - 1 - lastMove.startRow) * SQ_SIZE))
            screen.blit(s, ((DIMENSION - 1 - lastMove.endColumn) * SQ_SIZE,
                            (DIMENSION - 1 - lastMove.endRow) * SQ_SIZE))


def drawGameState(screen, gameState, validMoves, selectedSq, playerColor):
    drawBoard(screen)
    highlightLastMove(screen, gameState, playerColor)
    highlightSq(screen, gameState, validMoves, selectedSq, playerColor)
    drawPieces(screen, gameState.board, playerColor)


def drawBoard(screen):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = COLORS[(row + column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board, playerColor):
    if playerColor:
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                piece = board[row][column]
                if piece != "--":
                    screen.blit(IMAGES[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    else:
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                piece = board[DIMENSION - row - 1][DIMENSION - column - 1]
                if piece != "--":
                    screen.blit(IMAGES[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawEndGameText(screen, text):
    font = pygame.font.SysFont("Helvetica", 32, True, False)
    textObj = font.render(text, False, pygame.Color("gray"))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObj.get_width() / 2,
                                                         HEIGHT / 2 - textObj.get_height() / 2)
    screen.blit(textObj, textLocation)
    textObj = font.render(text, False, pygame.Color("black"))
    screen.blit(textObj, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
