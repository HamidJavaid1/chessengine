# chessengine.py

from shutil import move


class GameState:
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
        self.movefunctions = {
            'p': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }
        self.whitetomove = True
        self.movelog = []
        self.WhiteKingLocation = (7, 4)
        self.BlackKingLocation = (0, 4)
        self.checkmate = False
        self.Stalemate = False
        self.enpassantPossible = ()
        self.currentcastlingrights = Castleright(True, True, True, True)
        self.castlerightlog = [Castleright(self.currentcastlingrights.wks, self.currentcastlingrights.bks,
                                           self.currentcastlingrights.wqs, self.currentcastlingrights.bqs)]

    def makemove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.piecemoved
        if move.isenpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        self.whitetomove = not self.whitetomove
        if move.piecemoved == 'wK':
            self.WhiteKingLocation = (move.endRow, move.endCol)
        elif move.piecemoved == 'bK':
            self.BlackKingLocation = (move.endRow, move.endCol)
        if move.isPawnromotion:
            self.board[move.endRow][move.endCol] = move.piecemoved[0] + 'Q'
        if move.piecemoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()
        self.castlerightlog.append(Castleright(self.currentcastlingrights.wks, self.currentcastlingrights.bks,
                                               self.currentcastlingrights.wqs, self.currentcastlingrights.bqs))
        self.updatecastlingrights(move)
        if move.isCastlemove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'
        self.movelog.append(move)

    def undomove(self):
            if len(self.movelog)==0:
                return
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.piecemoved
            self.board[move.endRow][move.endCol] = move.piececaptured
            self.whitetomove = not self.whitetomove
            if move.piecemoved == 'wK':
                self.WhiteKingLocation = (move.startRow, move.startCol)
            elif move.piecemoved == 'bK':
                self.BlackKingLocation = (move.startRow, move.startCol)
            if move.isenpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.piececaptured
            self.castlerightlog.pop()
            self.currentcastlingrights = Castleright(self.castlerightlog[-1].wks, self.castlerightlog[-1].bks,
                                                     self.castlerightlog[-1].wqs, self.castlerightlog[-1].bqs)
            if move.isCastlemove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"


    def updatecastlingrights(self, move):
        if move.piecemoved == 'wK':
            self.currentcastlingrights.wks = False
            self.currentcastlingrights.wqs = False
        elif move.piecemoved == 'bK':
            self.currentcastlingrights.bks = False
            self.currentcastlingrights.bqs = False
        elif move.piecemoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentcastlingrights.wqs = False
                elif move.startCol == 7:
                    self.currentcastlingrights.wks = False
        elif move.piecemoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentcastlingrights.bqs = False
                elif move.startCol == 7:
                    self.currentcastlingrights.bks = False
        # Fix: Check if a rook was captured on a castling square
        if move.piececaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentcastlingrights.wqs = False
                elif move.endCol == 7:
                    self.currentcastlingrights.wks = False
        elif move.piececaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentcastlingrights.bqs = False
                elif move.endCol == 7:
                    self.currentcastlingrights.bks = False


    def getvalidmove(self):
        for log in self.castlerightlog:
            print(log.wks,log.wqs,log.bks,log.bqs,end=" ")
            print()
        tempEnpassantPossible = self.enpassantPossible
        tempCastleright = Castleright(self.currentcastlingrights.wks, self.currentcastlingrights.bks,
                                      self.currentcastlingrights.wqs, self.currentcastlingrights.bqs)

        moves = self.get_all_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.makemove(moves[i])
            self.whitetomove = not self.whitetomove
            if self.inCheck():
                moves.remove(moves[i])
            self.whitetomove = not self.whitetomove
            self.undomove()

        if self.whitetomove:
            self.getCastleMoves(self.WhiteKingLocation[0], self.WhiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.BlackKingLocation[0], self.BlackKingLocation[1], moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.Stalemate = True

        self.currentcastlingrights = tempCastleright
        self.enpassantPossible = tempEnpassantPossible
        return moves

    def inCheck(self):
        if self.whitetomove:
            return self.squareunderattack(self.WhiteKingLocation[0], self.WhiteKingLocation[1])
        else:
            return self.squareunderattack(self.BlackKingLocation[0], self.BlackKingLocation[1])

    def squareunderattack(self, r, c):
        self.whitetomove = not self.whitetomove
        opmoves = self.get_all_possible_moves(inCheckTestMode=True)
        self.whitetomove = not self.whitetomove
        for move in opmoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def get_all_possible_moves(self, inCheckTestMode=False):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "--":
                    turn = piece[0]
                    if (turn == 'w' and self.whitetomove) or (turn == 'b' and not self.whitetomove):
                        if piece[1] == 'K':
                            self.movefunctions['K'](r, c, moves, inCheckTestMode)  # ✅ fixed line
                        else:
                            self.movefunctions[piece[1]](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.whitetomove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, enpassantMove=True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, enpassantMove=True))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, enpassantMove=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, enpassantMove=True))

    def get_rook_moves(self, r, c, moves):
        directions = [(-1,0), (0,-1), (1,0), (0,1)]
        enemy_color = 'b' if self.whitetomove else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, r, c, moves):
        knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
        ally_color = 'w' if self.whitetomove else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        enemy_color = 'b' if self.whitetomove else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves, inCheckTestMode=False):
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        ally_color = 'w' if self.whitetomove else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == '--' or end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))
        if not inCheckTestMode:
            self.getCastleMoves(r, c, moves)

    def getCastleMoves(self, r, c, moves):
        if self.squareunderattack(r, c):
            return
        if self.whitetomove and (r, c) == (7, 4):
            if self.currentcastlingrights.wks:
                self.getKingsideCastleMove(r, c, moves)
            if self.currentcastlingrights.wqs:
                self.getQueensideCastleMove(r, c, moves)
        elif not self.whitetomove and (r, c) == (0, 4):
            if self.currentcastlingrights.bks:
                self.getKingsideCastleMove(r, c, moves)
            if self.currentcastlingrights.bqs:
                self.getQueensideCastleMove(r, c, moves)

    def getKingsideCastleMove(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareunderattack(r, c+1) and not self.squareunderattack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastlemove=True))

    def getQueensideCastleMove(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareunderattack(r, c-1) and not self.squareunderattack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastlemove=True))



class Castleright:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsquare, endsquare, board, enpassantMove=False, isCastlemove=False):
        self.startRow = startsquare[0]
        self.startCol = startsquare[1]
        self.endRow = endsquare[0]
        self.endCol = endsquare[1]
        self.piecemoved = board[self.startRow][self.startCol]
        self.piececaptured = board[self.endRow][self.endCol]

        self.isPawnromotion = (self.piecemoved == 'wp' and self.endRow == 0) or (self.piecemoved == 'bp' and self.endRow == 7)

        self.isenpassantMove = enpassantMove
        if self.isenpassantMove:
            self.piececaptured = 'bp' if self.piecemoved == 'wp' else 'wp'

        self.isCastlemove = isCastlemove

        self.moveid = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveid == other.moveid
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
