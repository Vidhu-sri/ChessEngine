import pygame as p
import ChessEngine
import ChessAI


#TO DEFINE
# - size
# - dimension
# - sq.size
# - max fps
# - global dictionary of images

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH//DIMENSION
MAX_FPS = 20
IMAGES = {}


def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR','bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR','wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f'images/{piece}.png'), (SQ_SIZE,SQ_SIZE))

#driver code
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    gameOver = False
    playerOne = True  # True means white is controlled by a human.
    playerTwo = False  # False means black is controlled by the AI.

    sqSelected = ()
    playerClicks= []
 
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():


            if e.type == p.QUIT:
                running = False
            
            #try drag and drop also 
            elif e.type == p.MOUSEBUTTONDOWN and not gameOver and humanTurn:
                pos = p.mouse.get_pos()
                row = pos[1]//SQ_SIZE
                col = pos[0]//SQ_SIZE
                clickedPiece = gs.board[row][col]

                if (row,col) == sqSelected:
                    sqSelected = ()
                    playerClicks = []
                elif not playerClicks:
                    if clickedPiece != '--' and clickedPiece[0] == ('w' if gs.whiteToMove else 'b'):
                        sqSelected = (row,col)
                        playerClicks = [sqSelected]
                else:
                    move = ChessEngine.Move(playerClicks[0], (row,col), gs.board)
                    print(move.getChessNotation())

                    if move in validMoves:
                        gs.makemove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    elif clickedPiece != '--' and clickedPiece[0] == ('w' if gs.whiteToMove else 'b'):
                        sqSelected = (row,col)
                        playerClicks = [sqSelected]
                    else:
                        sqSelected = ()
                        playerClicks = []
                        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undomove()
                    if not playerTwo and len(gs.movelog) > 0:
                        gs.undomove()
                    moveMade = True
                    gameOver = False
        
        if not gameOver and not humanTurn and not moveMade:
            AIMove = ChessAI.findBestMove(gs, validMoves)
            if AIMove is None:
                gameOver = True
            else:
                print(AIMove.getChessNotation())
                gs.makemove(AIMove)
                moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            if gs.checkMate or gs.staleMate:
                gameOver = True
         
        drawGameState(screen,gs,validMoves,sqSelected)
        if gameOver:
            if gs.staleMate:
                drawEndGameText(screen, 'Stalemate')
            else:
                winner = 'Black' if gs.whiteToMove else 'White'
                drawEndGameText(screen, winner + ' wins by checkmate')
        clock.tick(MAX_FPS)
        p.display.flip()




def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)


#drawboard , drawpieces can be handled in a single function 
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[(i+j)%2]
            p.draw.rect(screen,color,p.Rect((j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE)))

def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected == ():
        return
    row, col = sqSelected
    if gs.board[row][col] == '--' or gs.board[row][col][0] != ('w' if gs.whiteToMove else 'b'):
        return

    surface = p.Surface((SQ_SIZE,SQ_SIZE))
    surface.set_alpha(100)
    surface.fill(p.Color('blue'))
    screen.blit(surface, (col*SQ_SIZE,row*SQ_SIZE))
    surface.fill(p.Color('yellow'))
    for move in validMoves:
        if move.startrow == row and move.startcol == col:
            screen.blit(surface, (move.endcol*SQ_SIZE,move.endrow*SQ_SIZE))

def drawPieces(screen,board):

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if board[i][j] == '--':
                continue
            screen.blit(IMAGES[board[i][j]], (j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def drawEndGameText(screen,text):
    font = p.font.SysFont('Helvetica', 32, True, False)
    textObject = font.render(text, False, p.Color('black'))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('gray'))
    screen.blit(textObject, textLocation.move(2,2))



if __name__ == '__main__':
    main()
