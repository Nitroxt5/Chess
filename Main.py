import Engine
import tkinter as tk
from PIL import Image, ImageTk
import AI
from math import ceil, floor
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
SQ_SIZE = BOARD_HEIGHT // Engine.DIMENSION
IMAGES = {}


def loadImages():
    for piece in Engine.COLORED_PIECES:
        IMAGES[piece] = ImageTk.PhotoImage(Image.open(f"images/{piece}.png").resize((SQ_SIZE, SQ_SIZE)))
    IMAGES["icon"] = ImageTk.PhotoImage(Image.open(f"images/icon.png").resize((SQ_SIZE, SQ_SIZE)))
    IMAGES["brown"] = ImageTk.PhotoImage(Image.open(f"images/brown.png").resize((SQ_SIZE, SQ_SIZE)))
    IMAGES["yellow"] = ImageTk.PhotoImage(Image.open(f"images/yellow.png").resize((SQ_SIZE, SQ_SIZE)))
    IMAGES["blue"] = ImageTk.PhotoImage(Image.open(f"images/blue.png").resize((SQ_SIZE, SQ_SIZE)))
    IMAGES["board"] = ImageTk.PhotoImage(Image.open(f"images/board.png").resize((BOARD_HEIGHT, BOARD_WIDTH)))


whitePlayer = True
blackPlayer = False
playerColor = False if blackPlayer and not whitePlayer else True

gameState = Engine.GameState()
validMoves = gameState.getValidMoves()
playerTurn = (gameState.whiteTurn and whitePlayer) or (not gameState.whiteTurn and blackPlayer)
moveMade = False
gameOver = False
AIThinking = False
AIProcess = Process()
returnQ = Queue()
selectedSq = ()
clicks = []
AIThinkingTime = 0
AIPositionCounter = 0


def onQuit():
    global AIThinking, AIProcess, gameState
    if AIThinking:
        AIProcess.terminate()
        AIThinking = False
    print(gameState.gameLog)
    if not whitePlayer and not blackPlayer:
        moveCountCeil = len(gameState.gameLog)
        moveCountFloor = len(gameState.gameLog)
    else:
        moveCountCeil = ceil(len(gameState.gameLog) / 2)
        moveCountFloor = floor(len(gameState.gameLog) / 2)
    print(f"Moves: {moveCountCeil}")
    print(f"Overall thinking time: {AIThinkingTime}")
    print(f"Overall positions calculated: {AIPositionCounter}")
    if moveCountFloor != 0 and AIPositionCounter != 0:
        print(f"Average time per move: {AIThinkingTime / moveCountFloor}")
        print(f"Average calculated positions per move: {AIPositionCounter / moveCountFloor}")
        print(f"Average time per position: {AIThinkingTime / AIPositionCounter}")
    screen.destroy()


def undo(event):
    global gameState, moveMade, gameOver, AIThinking, playerTurn, AIProcess, validMoves
    gameState.undoMove()
    validMoves = gameState.getValidMoves()
    moveMade = True
    if gameOver:
        gameOver = False
    if AIThinking:
        AIProcess.terminate()
        AIThinking = False
    playerTurn = (gameState.whiteTurn and whitePlayer) or (not gameState.whiteTurn and blackPlayer)
    drawGameState()


def remake(event):
    global gameState, validMoves, selectedSq, clicks, AIThinkingTime, AIPositionCounter, gameOver, playerTurn, moveMade, AIThinking, AIProcess
    gameState = Engine.GameState()
    validMoves = gameState.getValidMoves()
    selectedSq = ()
    clicks = []
    AIThinkingTime = 0
    AIPositionCounter = 0
    if gameOver:
        gameOver = False
    moveMade = False
    if AIThinking:
        AIProcess.terminate()
        AIThinking = False
    playerTurn = (gameState.whiteTurn and whitePlayer) or (not gameState.whiteTurn and blackPlayer)
    drawGameState()


def mouseOnClick(event):
    global gameState, validMoves, selectedSq, clicks, moveMade, gameOver, playerTurn
    if playerTurn:
        if not gameOver:
            x, y = event.x, event.y
            column = x // SQ_SIZE
            row = y // SQ_SIZE
            if not playerColor:
                column = Engine.DIMENSION - column - 1
                row = Engine.DIMENSION - row - 1
            if selectedSq == (column, row) or column > 7 or column < 0 or row > 7 or row < 0:
                selectedSq = ()
                clicks = []
            else:
                selectedSq = (column, row)
                clicks.append(selectedSq)
            if len(clicks) == 2 and playerTurn:
                startSq = Engine.ONE >> (8 * clicks[0][1] + clicks[0][0])
                endSq = Engine.ONE >> (8 * clicks[1][1] + clicks[1][0])
                move = Engine.Move(startSq, endSq, gameState)
                for validMove in validMoves:
                    if move == validMove:
                        gameState.makeMove(validMove)
                        moveMade = True
                        selectedSq = ()
                        clicks = []
                        break
                if not moveMade:
                    clicks = [selectedSq]
        drawGameState()
        if moveMade:
            validMoves = gameState.getValidMoves()
            gameOverCheck()
            moveMade = False
            playerTurn = (gameState.whiteTurn and whitePlayer) or (not gameState.whiteTurn and blackPlayer)
        if not playerTurn:
            AIControl()


def AIControl():
    global gameState, validMoves, gameOver, playerTurn, AIThinking, AIProcess, AIThinkingTime, AIPositionCounter, moveMade, selectedSq, clicks
    playerTurn = (gameState.whiteTurn and whitePlayer) or (not gameState.whiteTurn and blackPlayer)
    if not gameOver and not playerTurn:
        if not AIThinking:
            print("thinking...")
            print(validMoves)
            AIThinking = True
            AIProcess = Process(target=AI.negaScoutMoveAI, args=(gameState, validMoves, returnQ))
            AIProcess.start()
        if not AIProcess.is_alive():
            AIMove, thinkingTime, positionCounter = returnQ.get()
            AIThinkingTime += thinkingTime
            AIPositionCounter += positionCounter
            print("came up with a move")
            print(f"Thinking time: {thinkingTime} s")
            print(f"Positions calculated: {positionCounter}")
            if AIMove is None:
                AIMove = AI.randomMoveAI(validMoves)
                print("made a random move")
            gameState.makeMove(AIMove)
            moveMade = True
            AIThinking = False
            selectedSq = ()
            clicks = []
    if moveMade:
        validMoves = gameState.getValidMoves()
        drawGameState()
        gameOverCheck()
        playerTurn = (gameState.whiteTurn and whitePlayer) or (not gameState.whiteTurn and blackPlayer)
        moveMade = False
    if not gameOver:
        screen.after(100, AIControl)


def gameOverCheck():
    global gameState, gameOver
    if gameState.checkmate:
        gameOver = True
        if gameState.whiteTurn:
            drawText("Black win by checkmate")
        else:
            drawText("White win by checkmate")
    elif gameState.stalemate:
        gameOver = True
        drawText("Stalemate")
    # if len(gameState.gameLog) == 40:
    #     gameOver = True


def highlightSq():
    global gameState, selectedSq
    if selectedSq != ():
        square = Engine.ONE >> (8 * selectedSq[1] + selectedSq[0])
        piece = gameState.getPieceBySquare(square)
        if piece is not None:
            if playerColor:
                canvas.create_image(selectedSq[0] * SQ_SIZE, selectedSq[1] * SQ_SIZE, anchor="nw", image=IMAGES["brown"], tags="move")
            else:
                c = Engine.DIMENSION - 1 - selectedSq[0]
                r = Engine.DIMENSION - 1 - selectedSq[1]
                canvas.create_image(c * SQ_SIZE, r * SQ_SIZE, anchor="nw", image=IMAGES["brown"], tags="move")
            if piece[0] == ("w" if gameState.whiteTurn else "b"):
                for move in validMoves:
                    if move.startSquare == square:
                        if playerColor:
                            canvas.create_image((move.endLoc % 8) * SQ_SIZE, (move.endLoc // 8) * SQ_SIZE, anchor="nw", image=IMAGES["yellow"], tags="move")
                        else:
                            r = Engine.DIMENSION - 1 - move.endLoc // 8
                            c = Engine.DIMENSION - 1 - move.endLoc % 8
                            canvas.create_image(c * SQ_SIZE, r * SQ_SIZE, anchor="nw", image=IMAGES["yellow"], tags="move")


def highlightLastMove():
    global gameState
    if len(gameState.gameLog) != 0:
        lastMove = gameState.gameLog[-1]
        if playerColor:
            canvas.create_image((lastMove.startLoc % 8) * SQ_SIZE, (lastMove.startLoc // 8) * SQ_SIZE, anchor="nw", image=IMAGES["blue"], tags="move")
            canvas.create_image((lastMove.endLoc % 8) * SQ_SIZE, (lastMove.endLoc // 8) * SQ_SIZE, anchor="nw", image=IMAGES["blue"], tags="move")
        else:
            c = Engine.DIMENSION - 1 - lastMove.startLoc % 8
            r = Engine.DIMENSION - 1 - lastMove.startLoc // 8
            canvas.create_image(c * SQ_SIZE, r * SQ_SIZE, anchor="nw", image=IMAGES["blue"], tags="move")
            c = Engine.DIMENSION - 1 - lastMove.endLoc % 8
            r = Engine.DIMENSION - 1 - lastMove.endLoc // 8
            canvas.create_image(c * SQ_SIZE, r * SQ_SIZE, anchor="nw", image=IMAGES["blue"], tags="move")


def drawGameState():
    canvas.delete("move")
    highlightLastMove()
    highlightSq()
    drawPieces()
    canvas.place(x=0, y=0, anchor="nw")


def drawBoard():
    canvas.create_image(0, 0, anchor="nw", image=IMAGES["board"])


def drawPieces():
    global gameState
    if playerColor:
        for piece in Engine.COLORED_PIECES:
            splitPositions = Engine.numSplit(gameState.bbOfPieces[piece])
            for position in splitPositions:
                pos = Engine.getPower(position)
                canvas.create_image((pos % 8) * SQ_SIZE, (pos // 8) * SQ_SIZE, anchor="nw", image=IMAGES[piece], tags="move")
    else:
        for piece in Engine.COLORED_PIECES:
            splitPositions = Engine.numSplit(gameState.bbOfPieces[piece])
            for position in splitPositions:
                pos = 63 - Engine.getPower(position)
                canvas.create_image((pos % 8) * SQ_SIZE, (pos // 8) * SQ_SIZE, anchor="nw", image=IMAGES[piece], tags="move")


def findCenter(item):
    coords = canvas.bbox(item)
    xOffset = (BOARD_WIDTH // 2) - ((coords[2] - coords[0]) // 2)
    yOffset = (BOARD_HEIGHT // 2) - ((coords[3] - coords[1]) // 2)
    return xOffset, yOffset


def drawText(text: str):
    txt1 = canvas.create_text(0, 0, text=text, font=("Helvetica", 20, "bold"), justify="center", fill="light gray", anchor="nw", tags="move")
    txt2 = canvas.create_text(2, 2, text=text, font=("Helvetica", 20, "bold"), justify="center", anchor="nw", tags="move")
    x, y = findCenter(txt1)
    canvas.move(txt1, x, y)
    canvas.move(txt2, x, y)


if __name__ == "__main__":
    screen = tk.Tk()
    loadImages()
    canvas = tk.Canvas(screen, height=BOARD_HEIGHT, width=BOARD_WIDTH, highlightthickness=0)
    screen.title("SwiChess")
    screen.iconphoto(False, IMAGES["icon"])
    screen.resizable(False, False)
    screen.geometry(f"{BOARD_WIDTH}x{BOARD_HEIGHT}")

    screen.bind("<Button-1>", mouseOnClick)
    screen.bind("u", undo)
    screen.bind("r", remake)
    screen.protocol("WM_DELETE_WINDOW", onQuit)

    drawBoard()
    drawGameState()
    AIControl()
    screen.mainloop()
