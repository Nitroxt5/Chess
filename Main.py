import Engine
import pygame

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

    loadImages()
    pygame.display.set_caption("SwiChess")
    pygame.display.set_icon(IMAGES["icon"])
    selectedSq = ()
    clicks = []

    # working = True
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # working = False
                quit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = pygame.mouse.get_pos()
                    column = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if selectedSq == (column, row):
                        selectedSq = ()
                        clicks = []
                    else:
                        selectedSq = (column, row)
                        clicks.append(selectedSq)
                    if len(clicks) == 2:
                        move = Engine.Move(clicks[0], clicks[1], gameState.board)
                        # print(move.getMoveNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                selectedSq = ()
                                clicks = []
                        if not moveMade:
                            clicks = [selectedSq]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_u:
                    gameState.undoMove()
                    moveMade = True
                if e.key == pygame.K_r:
                    gameState = Engine.GameState()
                    validMoves = gameState.getValidMoves()
                    selectedSq = ()
                    clicks = []
                    moveMade = False
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        drawGameState(screen, gameState, validMoves, selectedSq)
        if gameState.checkmate:
            gameOver = True
            if gameState.whiteTurn:
                drawText(screen, "Black win by checkmate")
            else:
                drawText(screen, "White win by checkmate")
        elif gameState.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")
        pygame.display.flip()


def highlightSq(screen, gameState, validMoves, selectedSq):
    if selectedSq != ():
        column, row = selectedSq
        if gameState.board[row][column][0] == ("w" if gameState.whiteTurn else "b"):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.fill(pygame.Color(110, 90, 0))
            screen.blit(s, (column * SQ_SIZE, row * SQ_SIZE))
            s.set_alpha(100)
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.startColumn == column and move.startRow == row:
                    screen.blit(s, (move.endColumn * SQ_SIZE, move.endRow * SQ_SIZE))


def highlightLastMove(screen, gameState):
    if len(gameState.gameLog) != 0:
        lastMove = gameState.gameLog[-1]
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(pygame.Color(182, 255, 0))
        screen.blit(s, (lastMove.startColumn * SQ_SIZE, lastMove.startRow * SQ_SIZE))
        screen.blit(s, (lastMove.endColumn * SQ_SIZE, lastMove.endRow * SQ_SIZE))


def drawGameState(screen, gameState, validMoves, selectedSq):
    drawBoard(screen)
    highlightLastMove(screen, gameState)
    highlightSq(screen, gameState, validMoves, selectedSq)
    drawPieces(screen, gameState.board)


def drawBoard(screen):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = COLORS[(row + column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawText(screen, text):
    font = pygame.font.SysFont("Helvetica", 32, True, False)
    textObj = font.render(text, False, pygame.Color("gray"))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObj.get_width() / 2,
                                                         HEIGHT / 2 - textObj.get_height() / 2)
    screen.blit(textObj, textLocation)
    textObj = font.render(text, False, pygame.Color("black"))
    screen.blit(textObj, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
