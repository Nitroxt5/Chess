import Engine
import pygame

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["icon", "wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("Chess/images/" + piece + ".png"),
                                               (SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gameState = Engine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False

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
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)


def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("dark gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[(row + column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
