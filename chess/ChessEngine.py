
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
        
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K':self.getKingMoves}

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
                
                    self.moveFunctions[piece](r,c,moves) # calls the appropriate move functions
        return moves
    
    def getPawnMoves(self, r, c, moves):
        
        color = self.board[r][c][0]
        ispiece = lambda r,c: (self.board[r][c] !='--')

        # first pawn move
        firstmove =  (color == 'b' and r == 1 and not self.whiteToMove) or (color == 'w' and r== 6 and self.whiteToMove)
        
        direction = -1 if color == 'w' else 1

        if r+direction<=7  and not ispiece(r+direction,c):
            moves.append(Move((r,c),(r+direction,c), self.board)) 

        if firstmove and not ispiece(r+2*direction,c):
                moves.append(Move((r,c), (r+2*direction,c) , self.board)) 
    
        # killing
    
        next = r-1 if color == 'w' else r+1
        for i in (-1,1):
            if 0<=next<=7 and 0<=c+i<=7 and ispiece(next,c+i) and self.board[next][c+i][0] != color:
                moves.append(Move((r,c),(next,c+i), self.board))


        #119-w, 98 - b

        #en passant
        # 

       
        
    def getRookMoves(self,r,c,moves):
        
        ispiece = lambda r,c: self.board[r][c] != '--'

        i = 1
        #same file
        for i in range(r+1,8):
            if ispiece(i,c):
                break
            moves.append(Move((r,c), (i,c), self.board))
        moves.append(Move((r,c), (i,c), self.board))  #capture
        

        for i in range(r-1,-1,-1):
            if ispiece(i,c):
                break
            moves.append(Move((r,c), (i,c), self.board))
        moves.append(Move((r,c), (i,c), self.board))  #capture
       
        
        #same rank
        for i in range(c+1,8):
            if ispiece(r,i):
                break
            moves.append(Move((r,c), (r,i), self.board))
        moves.append(Move((r,c), (r,i), self.board))    #capture

        for i in range(c-1,-1,-1):
            if ispiece(r,i):
                break
            moves.append(Move((r,c), (r,i), self.board))
        moves.append(Move((r,c), (r,i), self.board))    #capture
        


    def getKnightMoves(self,r,c,moves):
        pass
    def getBishopMoves(self,r,c,moves):
        pass
    def getKingMoves(self,r,c,moves):
        pass
    def getQueenMoves(self,r,c,moves):
        pass
                

        
    





class Move:


    RowtoRank = {7-i:chr(ord('0')+i) for i in range(8)}
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