import pygame as p
import ChessEngine


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
    loadImages()
    running = True

    sqSelected = ()
    playerClicks= []
 
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            #try drag and drop also 
            elif e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                row = pos[1]//SQ_SIZE
                col = pos[0]//SQ_SIZE

                if len(playerClicks) == 1:
                    initsq = playerClicks[-1]
                    if gs.board[initsq[0]][initsq[1]] == '--':
                        sqSelected = ()
                        playerClicks = []
                        continue
                    
                if (row,col) == sqSelected:
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) ==2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    gs.makemove(move)
                    sqSelected = ()
                    playerClicks = []

        
          
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)


#drawboard , drawpieces can be handled in a single function 
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[(i+j)%2]
            p.draw.rect(screen,color,p.Rect((j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE)))

def drawPieces(screen,board):

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if board[i][j] == '--':
                continue
            screen.blit(IMAGES[board[i][j]], (j*SQ_SIZE,i*SQ_SIZE,SQ_SIZE,SQ_SIZE))



if __name__ == '__main__':
    main()