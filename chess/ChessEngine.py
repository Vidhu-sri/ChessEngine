
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
    





class Move:

    RowtoRank = {8-i:chr(ord('0')+i) for i in range(8)}
    RanktoRow = {y:x for x,y in RowtoRank.items()}
    FiletoCol = {chr(ord('a')+i):i for i in range(7)}
    ColtoFile = {y:x for x,y in FiletoCol.items()}


    def __init__(self, startsq, endsq, board):    
        self.startrow, self.startcol = startsq[0], startsq[1]
        self.endrow, self.endcol = endsq[0], endsq[1]
        self.pieceCaptured = board[self.startrow][self.startcol]
        self.pieceMoved = board[self.startrow][self.startcol]

    #change this later to real chess notation
    def getChessNotation(self):
        return self.getRankFile(self.startrow,self.startcol) + self.getRankFile(self.endrow,self.endcol)

    def getRankFile(self,row,col):
        return self.ColtoFile[col]+self.RowtoRank[row]
