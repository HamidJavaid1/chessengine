class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whitetomove = True
        self.movelog = []

    def makemove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.piecemoved
        self.movelog.append(move)
        self.whitetomove = not self.whitetomove
    def undomove(self):
        if len(self.movelog)!=0:
         move = self.movelog.pop()
         self.board[move.startRow][move.startCol] = move.piecemoved
         self.board[move.endRow][move.endCol] = move.piececaptured
         self.whitetomove=not self.whitetomove
    
    def getvalidmove(self):
        return self.Allpossiblemove()
     #move with checks
     
    def Allpossiblemove(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn=='w'and self.whitetomove) and(   turn=='b'and not self.whitetomove): 
                   piece=self.board[r][c][1]
                   if piece=='p':
                       moves=self.getpawnsmove(r,c,moves)
                   elif piece=='R':
                       moves=self.getrookmove(r,c,moves)
                   elif piece=='N':
                       moves=self.getknightmove(r,c,moves)
                       
    def getpawnmove( self,r,c,moves):
         pass
             
              #move without checks
    


class Move():
    ranksToRow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRow.items()}
    filesToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCol.items()}

    def __init__(self, startsquare, endsquare, board):
        self.startRow = startsquare[0]
        self.startCol = startsquare[1]
        self.endRow = endsquare[0]
        self.endCol = endsquare[1]
        self.piecemoved = board[self.startRow][self.startCol]
        self.piececaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankfiles(self.startRow, self.startCol) + self.getRankfiles(self.endRow, self.endCol)

    def getRankfiles(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
