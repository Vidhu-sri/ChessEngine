
#to handle current state of the board
#determines valid moves as well



#TO TRACK

#whose turn is it
#movelog
#can castle?
import itertools

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
        self.ispiece = lambda r,c: self.board[r][c] != '--'
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)



    def makemove(self, move):
        self.board[move.startrow][move.startcol] = '--'
        self.board[move.endrow][move.endcol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove
        #update the king's location if moved
        if move.pieceMoved =='wK':
            self.whiteKingLocation = (move.endrow,move.endcol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endrow,move.endcol)

    #undo the last move made
    def undomove(self):
        if not self.movelog:
            return
        move = self.movelog.pop()
        self.board[move.endrow][move.endcol] = move.pieceCaptured
        self.board[move.startrow][move.startcol] = move.pieceMoved
        self.whiteToMove = not self.whiteToMove
        #update the king's position if required
        if move.pieceMoved =='wK':
            self.whiteKingLocation = (move.startrow,move.startcol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startrow,move.startcol)

    
    #generate all possible moves
    #for each move, make the move
    #generate all possible opponent's moves
    #for each of your oppenent's moves, see if they attack your king
    # if they attack your king, not a valid move
    def getValidMoves(self):
        moves =  self.getAllPossibleMoves()
        for i in range(len(moves)-1,-1,-1):
            self.makemove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undomove()
        return moves



    def inCheck(self):
        
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endrow == r and move.endcol == c:
                return True
        return False



    
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
        

        # first pawn move
        firstmove =  (color == 'b' and r == 1 and not self.whiteToMove) or (color == 'w' and r== 6 and self.whiteToMove)
        
        direction = -1 if color == 'w' else 1

        if r+direction<=7  and not self.ispiece(r+direction,c):
            moves.append(Move((r,c),(r+direction,c), self.board)) 

        if firstmove and not self.ispiece(r+2*direction,c):
                moves.append(Move((r,c), (r+2*direction,c) , self.board)) 
    
        # killing
    
        next = r-1 if color == 'w' else r+1
        for i in (-1,1):
            if 0<=next<=7 and 0<=c+i<=7 and self.ispiece(next,c+i) and self.board[next][c+i][0] != color:
                moves.append(Move((r,c),(next,c+i), self.board))


        #en passant
        if color == 'b' and r == 4:
            move = self.movelog[-1]
            if abs(move.endcol - c) == 1 and move.endrow == r:
                moves.append(Move((r,c),(move.endrow+1,move.endcol), self.board))
        if color == 'w' and r == 3:
            move = self.movelog[-1]
            if abs(move.endcol - c) == 1 and move.endrow == r:
                moves.append(Move((r,c),(move.endrow-1,move.endcol), self.board))


       
        
    def getRookMoves(self,r,c,moves):
        
        
        color = self.board[r][c][0]

        i = 1
        #same file
        for i in range(r+1,8):
            if self.ispiece(i,c):
                break
            moves.append(Move((r,c), (i,c), self.board))
        if self.board[i][c][0] != color:
            moves.append(Move((r,c), (i,c), self.board))  #capture
        

        for i in range(r-1,-1,-1):
            if self.ispiece(i,c):
                break
            moves.append(Move((r,c), (i,c), self.board))
        if self.board[i][c][0] != color:
            moves.append(Move((r,c), (i,c), self.board))  #capture
       
        
        #same rank
        for i in range(c+1,8):
            if self.ispiece(r,i):
                break
            moves.append(Move((r,c), (r,i), self.board))
        if self.board[r][i][0] != color:
            moves.append(Move((r,c), (r,i), self.board))    #capture

        for i in range(c-1,-1,-1):
            if self.ispiece(r,i):
                break
            moves.append(Move((r,c), (r,i), self.board))
        if self.board[r][i][0] != color:
            moves.append(Move((r,c), (r,i), self.board))    #capture
        
    

    def getKnightMoves(self,r,c,moves):

        color = self.board[r][c][0]
        reach = [(r+2,c+1), (r+2,c-1), (r-2,c+1), (r-2,c-1), (r+1,c+2), (r-1,c+2), (r+1,c-2), (r-1,c-2)]
        withinboard = lambda r,c: (0<=r<=7 and 0<=c<=7)
        


        for move in reach:
            if withinboard(move[0], move[1]):
                if not self.ispiece(move[0], move[1]):
                    moves.append(Move((r,c), move, self.board))
                elif self.ispiece(move[0], move[1]) and self.board[move[0]][move[1]][0] != color:
                    moves.append(Move((r,c), move, self.board))

                    
        


    def getBishopMoves(self,r,c,moves):
        
        directions = [(1,-1), (-1,1), (1,1), (-1,-1)]
        withinboard = lambda r,c: (0<=r<=7 and 0<=c<=7)
        color = self.board[r][c][0]

        for dir in directions:
            i = 1
            while withinboard(r+dir[0]*i, c+dir[1]*i) and not self.ispiece(r+dir[0]*i, c+dir[1]*i):
                moves.append(Move((r,c), (r+dir[0]*i, c+dir[1]*i), self.board))
                i+=1
            if withinboard(r+dir[0]*i, c+dir[1]*i) and self.board[r+dir[0]*i][c+dir[1]*i][0] != color:
                moves.append(Move((r,c), (r+dir[0]*i, c+dir[1]*i), self.board))
    


    def getKingMoves(self,r,c,moves):

        directions = [*itertools.product((0,1,-1), repeat=2)]
        withinboard = lambda r,c: (0<=r<=7 and 0<=c<=7)
        color = self.board[r][c]
        directions.pop(0)

        for dir in directions:
            if withinboard(r+dir[0], c+dir[1]):
                if not self.ispiece(r+dir[0], c+dir[1]):
                    moves.append(Move((r,c), (r+dir[0], c+dir[1]), self.board))
                elif self.board[r+dir[0]][c+dir[1]][0] != color:
                    moves.append(Move((r,c), (r+dir[0], c+dir[1]), self.board))



        
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)

                



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