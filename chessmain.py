# displaying current game state object
import pygame as p
import chessengine

width = height = 512
Dimension = 8
Sqsize = height // Dimension
MaxFps = 15
IMAGES = {}

def load_images():
    pieces = ["wp", "bp", "wN", "bN", "wR", "bR", "wB", "bB", "wK", "bK", "wQ", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chesspieceimages/" + piece + ".png"), (Sqsize, Sqsize))

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.GameState()
    load_images()
    running = True
    Sqselected = ()
    playesclicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = location[1] // Sqsize
                col = location[0] // Sqsize
                piece = gs.board[row][col]

                if Sqselected == (row, col):
                    Sqselected = ()
                    playesclicks = []
                else:
                    # If first click, only allow selecting a piece of the current player
                    if len(playesclicks) == 0:
                        if piece != "--" and ((piece[0] == 'w' and gs.whitetomove) or (piece[0] == 'b' and not gs.whitetomove)):
                            Sqselected = (row, col)
                            playesclicks.append(Sqselected)
                    else:
                        Sqselected = (row, col)
                        playesclicks.append(Sqselected)

                if len(playesclicks) == 2:
                    move = chessengine.Move(playesclicks[0], playesclicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makemove(move)
                    Sqselected = ()
                    playesclicks = []
            elif e.type==p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undomove()



        drawgamestate(screen, gs)
        clock.tick(MaxFps)
        p.display.flip()

def drawgamestate(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color("dark green")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * Sqsize, r * Sqsize, Sqsize, Sqsize))

def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * Sqsize, r * Sqsize, Sqsize, Sqsize))

if __name__ == "__main__":
    main()
