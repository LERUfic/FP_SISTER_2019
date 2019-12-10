class SingleBoard:
    def __init__(self,board_id):
        self.player1 = False
        self.player2 = False
        self.pieces = 0
        self.board=[None for j in range(9)]
        self.id = board_id

    def isMyTurn(self,all_board):
        self.getPieces(all_board)
        if (self.pieces % 2) == 0:
            if self.player1 == True:
                return True
            else:
                return False
        else:
            if self.player1 == True:
                return False
            else:
                return True

    def joinGame(self,all_board):
        self.getPieces(all_board)
        if self.pieces == 0:
            self.player1 = True
            return 1
        elif self.pieces == 1:
            self.player2 = True
            return 2
        else:
            return -1

    def checkWinner(self,all_board):
        self.getPieces(all_board)
        pemenang = None
        #check horisontal
        index_horizontal = 0
        for i in range(3):
            if self.board[index_horizontal] == self.board[index_horizontal+1] and self.board[index_horizontal+1] == self.board[index_horizontal+2]:
                pemenang = self.board[index_horizontal]
                break
            else:
                index_horizontal = index_horizontal + 3
        
        #check vertikal
        index_vertikal = 0
        for i in range(3):
            if self.board[index_vertikal] == self.board[index_vertikal+3] and self.board[index_vertikal+3] == self.board[index_vertikal+6]:
                pemenang = self.board[index_vertikal]
                break
            else:
                index_vertikal = index_vertikal + 1

        #check diagonal
        if self.board[0] == self.board[4] and self.board[4] == self.board[8]:
            pemenang = self.board[0]
        if self.board[2] == self.board[4] and self.board[4] == self.board[6]:
            pemenang = self.board[2]

        return pemenang

    def extractBoard(self,all_board):
        self.board=[None for j in range(9)]
        if self.id == 0:
            self.board = [all_board[0][0],all_board[0][1],all_board[0][2], all_board[1][0],all_board[1][1],all_board[1][2], all_board[2][0],all_board[2][1],all_board[2][2]]
        elif self.id == 1:
            self.board = [all_board[0][3],all_board[0][4],all_board[0][5], all_board[1][3],all_board[1][4],all_board[1][5], all_board[2][3],all_board[2][4],all_board[2][5]]
        elif self.id == 2:
            self.board = [all_board[0][6],all_board[0][7],all_board[0][8], all_board[1][6],all_board[1][7],all_board[1][8], all_board[2][6],all_board[2][7],all_board[2][8]]
        elif self.id == 3:
            self.board = [all_board[3][0],all_board[3][1],all_board[3][2], all_board[4][0],all_board[4][1],all_board[4][2], all_board[5][0],all_board[5][1],all_board[5][2]]
        elif self.id == 4:
            self.board = [all_board[3][3],all_board[3][4],all_board[3][5], all_board[4][3],all_board[4][4],all_board[4][5], all_board[5][3],all_board[5][4],all_board[5][5]]
        elif self.id == 5:
            self.board = [all_board[3][6],all_board[3][7],all_board[3][8], all_board[4][6],all_board[4][7],all_board[4][8], all_board[5][6],all_board[5][7],all_board[5][8]]
        elif self.id == 6:
            self.board = [all_board[6][0],all_board[6][1],all_board[6][2], all_board[7][0],all_board[7][1],all_board[7][2], all_board[8][0],all_board[8][1],all_board[8][2]]
        elif self.id == 7:
            self.board = [all_board[6][3],all_board[6][4],all_board[6][5], all_board[7][3],all_board[7][4],all_board[7][5], all_board[8][3],all_board[8][4],all_board[8][5]]
        elif self.id == 8:
            self.board = [all_board[6][6],all_board[6][7],all_board[6][8], all_board[7][6],all_board[7][7],all_board[7][8], all_board[8][6],all_board[8][7],all_board[8][8]]

    def getPieces(self,all_board):
        self.extractBoard(all_board)
        countable = 0
        for i in range(9):
            if self.board[i] != None:
                countable = countable + 1
        self.pieces = countable

    def countPieces(self,all_board):
        self.getPieces(all_board)
        return self.pieces

    def countBoard(self,all_board):
        self.getPieces(all_board)
        return self.board
        return self.pieces
