
#to handle current state of the board
#determines valid moves as well



#TO TRACK

#whose turn is it
#movelog
#can castle?

class GameState:
    def __init__(self):
        
        self.board =  [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.whiteToMove = True
        self.movelog = []

    def makemove(self, move):
        self.board[move.startrow][move.startcol] = '--'
        self.board[move.endrow][move.endcol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove

    #undo the last move made
    def undomove(self):
        if not self.movelog:
            return
        move = self.movelog.pop()
        self.board[move.endrow][move.endcol] = move.pieceCaptured
        self.board[move.startrow][move.startcol] = move.pieceMoved
        self.whiteToMove = not self.whiteToMove
        
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                turn = self.board[r][c][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                
                if piece == 'p':
                    self.getPawnMoves(r,c,moves)
                elif piece == 'R':
                    self.getRookMoves(r,c,moves)
    
    def getPawnMoves(self, r, c, moves):
        pass
    def getRookMoves(self,r,c,moves):
        pass
                

        
    





class Move:

    RowtoRank = {8-i:chr(ord('0')+i) for i in range(8)}
    RanktoRow = {y:x for x,y in RowtoRank.items()}
    FiletoCol = {chr(ord('a')+i):i for i in range(8)}
    ColtoFile = {y:x for x,y in FiletoCol.items()}


    def __init__(self, startsq, endsq, board):    
        self.startrow, self.startcol = startsq[0], startsq[1]
        self.endrow, self.endcol = endsq[0], endsq[1]
        self.pieceCaptured = board[self.endrow][self.endcol]
        self.pieceMoved = board[self.startrow][self.startcol]
        self.moveID = self.startrow*1000 + self.startcol*100 + self.endrow*10 + self.endcol


    '''
    Overriding the equals method
    '''
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    #change this later to real chess notation
    def getChessNotation(self):
        return self.getRankFile(self.startrow,self.startcol) + self.getRankFile(self.endrow,self.endcol)

    def getRankFile(self,row,col):
        return self.ColtoFile[col]+self.RowtoRank[row]