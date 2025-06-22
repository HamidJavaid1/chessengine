import pygame as p
import chessengine
import smartmovefinder

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
    validmoves = gs.getvalidmove()
    movemade = False
    animate=False
    gameOver=False   
    playesone=True
    playertwo=False
    load_images()
    running = True
    Sqselected = ()
    playesclicks = []

    while running:
        humanturn=(gs.whitetomove and playesone) or (not gs.whitetomove and playertwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanturn:
                    location = p.mouse.get_pos()
                    row = location[1] // Sqsize
                    col = location[0] // Sqsize
                    piece = gs.board[row][col]

                    if Sqselected == (row, col):
                        Sqselected = ()
                        playesclicks = []
                    else:
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
                        for valid_move in validmoves:
                            if move == valid_move:
                                gs.makemove(valid_move)
                                animate=True
                                movemade = True
                                Sqselected = ()
                                playesclicks = []
                                break
                        if not movemade:
                            playesclicks = [Sqselected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undomove()
                    movemade = True
                    animate=False
                    gs.checkmate=False
                    gs.Stalemate=False                    
                if e.key == p.K_r:
                    gs=chessengine.GameState()
                    Sqselected = ()
                    playesclicks = []
                    movemade = False
                    animate=False
                    gameOver=False
                   
                    validmoves= gs.getvalidmove()

        # Ai move finder
        if not gameOver and not humanturn:
            AIMove=smartmovefinder.findbestmethod(gs,validmoves)
            if AIMove is None:
                AIMove=smartmovefinder.findrandommove(validmoves)
            gs.makemove(AIMove)
            movemade=True
            animate=True


        if movemade:
            if animate:
                animatemove(gs.movelog[-1],screen,gs.board,clock)
            validmoves = gs.getvalidmove()
            print(dir(smartmovefinder))

            movemade = False
            animate=False

        drawgamestate(screen, gs,validmoves,Sqselected )

        if gs.checkmate:
            gameOver=True
            if gs.whitetomove:
                drawText(screen,'Black Wins By Checkmate')
            else:
                drawText(screen,'White Wins By Checkmate')

        elif gs.Stalemate:
            gameOver=True
            drawText(screen,'Stalemate')
        clock.tick(MaxFps)
        p.display.flip()
def highlightMove(screen,gs,validmove,sqselected):
    if  sqselected!=():
        r,c=sqselected
        if gs.board[r][c][0]==('w' if gs.whitetomove else 'b'):
            s=p.Surface((Sqsize,Sqsize))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*Sqsize,r*Sqsize))

            s.fill(p.Color('yellow'))
            for move in validmove:
                if move.startRow==r and move.startCol==c:
                    screen.blit(s,(move.endCol*Sqsize,move.endRow*Sqsize))
            


def drawgamestate(screen, gs,validmove,sqselected):
    drawBoard(screen)
    highlightMove(screen,gs,validmove,sqselected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
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


def animatemove(move, screen, board, clock):
    DR = move.endRow - move.startRow
    DC = move.endCol - move.startCol
    frameperSquare = 10  # frames for one square
    farmecount = (abs(DR) + abs(DC)) * frameperSquare

    for frame in range(farmecount + 1):
        r, c = (move.startRow + DR * frame / farmecount,
                move.startCol + DC * frame / farmecount)

        drawBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * Sqsize, move.endRow * Sqsize, Sqsize, Sqsize)
        p.draw.rect(screen, color, endSquare)

        if move.piececaptured != '--':
            screen.blit(IMAGES[move.piececaptured], endSquare)  # ✅ FIXED LINE

        screen.blit(IMAGES[move.piecemoved], p.Rect(c * Sqsize, r * Sqsize, Sqsize, Sqsize))
        p.display.flip()
        clock.tick(60)

def drawText(screen,Text):
        font=p.font.SysFont("Helvtica",38,True,False)
        textObject=font.render(Text,0,p.Color('Red'))
        textLocation=p.Rect(0,0,width,height).move(width/2-textObject.get_width()/2,height/2-textObject.get_height()/2)
        screen.blit(textObject,textLocation)


if __name__ == "__main__":
    main()
