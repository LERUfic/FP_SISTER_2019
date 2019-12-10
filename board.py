import Pyro4
import pygame
import threading
import time
import singleboard
import player
pygame.init()

class clientproxy:
    def connect(self):
        uri = "PYRONAME:clientproxy@localhost:7777"
        gserver = Pyro4.Proxy(uri)
        return gserver

class TicTacToe:
    def __init__(self):
        self.screen=pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Tic Tac Toe")
        self.screen.fill((255,255,255))
        self.xo=[[None for j in range(9)] for i in range(9)]
        self.kotak=dict()
        self.button=dict()
        self.x0=200
        self.y0=100
        self.boardstatus=[0,0,0,0,0,0,0,0,0]
        # koordinat board x1,x2,y1,y2 
        self.board_loc=[[0,2,0,2],[3,5,0,2],[6,8,0,2],
                        [0,2,3,5],[3,5,3,5],[6,8,3,5],
                        [0,2,6,8],[3,5,6,8],[6,8,6,8]]
        self.pawn = 0
        self.board_id = -1
        self.current_board = None
        self.c = clientproxy()
        self.proxy = self.c.connect()

    def createBoard(self):
        self.createText("TicTacToe Gan","freesansbold.ttf",50,(0,0,0),640,50)
        for y in range(9):
            x1=self.x0
            for x in range(9):
                loc=str(x)+','+str(y)
                #(a,b)=x1 x2 y1 y2
                coordinate=str(x1)+" "+str(x1+60)+" "+str(self.y0)+" "+str(self.y0+60) 
                self.kotak[loc]=coordinate
                self.button[str(x)+' '+str(y)]=pygame.draw.rect(self.screen, (176, 175, 178),(x1,self.y0,60,60))
                x1=x1+65
            self.y0=self.y0+65
        pygame.display.update()

    def text_objects(self, text,font,color):
        textSurface = font.render(text,True,color)
        return textSurface, textSurface.get_rect()

    def createText(self, text,font,size,color,x,y):
        largeText = pygame.font.Font(font, size)
        TextSurf, TextRect = self.text_objects(text,largeText,color)
        TextRect.center=x,y
        self.screen.blit(TextSurf,TextRect)
        return TextSurf

    def createTempText(self, a,text,font,size,color,x,y):
        i=0
        largeText = pygame.font.Font(font, size)
        TextSurf, TextRect = self.text_objects(text,largeText,color)
        TextRect.center=x,y
        while i<3:
            # print(i)
            self.screen.blit(TextSurf,TextRect)
            time.sleep(1)
            i=i+1
            pygame.display.update()
        self.drawbox("",20,"freesansbold.ttf",(255,255,255),(800),(100),350,200,(0,0,0),(150,150,150))


    def draw_button(self,text,text_size,font,font_color,x,y,width,height,color1,color2,action=None,arg=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print click
        if x+width > mouse[0] > x and y+height > mouse[1] > y:
            pygame.draw.rect(self.screen, color2, (x,y,width,height))
            if click[0] == 1 and action != None and arg == None:
                action()
            elif click[0] == 1 and action != None and arg != None:
                action(arg)
        else:
            pygame.draw.rect(self.screen, color1, (x,y,width,height))
        self.createText(text,font,text_size,font_color,(x+(width/2)),(y+(height/2)))

    def drawbox(self,text,text_size,font,font_color,x,y,width,height,color1,color2,action=None,arg=None):    
        popupbox=pygame.draw.rect(self.screen, color1, (x,y,width,height))
        return popupbox

    def update_board_status(self,x,y):
        for i in range(len(self.board_loc)):
            if x>=self.board_loc[i][0] and x<=self.board_loc[i][1] and y>=self.board_loc[i][2] and y<=self.board_loc[i][3]:
                # print(i)
                self.boardstatus[i]=self.boardstatus[i]+1
                return i

    def getLatestBoard(self):
        '''
        This is for testing purpose only.
        The actual getLatestBoard will be pulling data from server using Pyro4,
        then that data will be decode because probably we will use pickle as object serialization then return it.
        '''
        # testing_board=[[None for j in range(9)] for i in range(9)]


        board = self.proxy.getboard()

        # # testing_board[2][1] = 1
        # testing_board[4][2] = 1
        # testing_board[6][3] = 1
        # testing_board[1][4] = 1
        # testing_board[2][8] = 1

        # testing_board[8][5] = 2
        # testing_board[7][6] = 2
        # testing_board[1][7] = 2
        # # testing_board[1][2] = 2
        # testing_board[4][3] = 2   


        return board

    def updateBoard(self):
        self.xo = self.getLatestBoard()

        for y in range(9):
            for x in range(9):
                if self.xo[x][y] == 1:
                    self.createText("X","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)
                elif self.xo[x][y] == 2:
                    self.createText("O","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)

        pygame.display.update()
        
        if self.current_board != None:
            pemenang = self.current_board.checkWinner(self.xo)
            if pemenang != None:
                # POP UP PEMENANG
                print(pemenang)
                saving_data = player.Player()
                saving_data.resetData()
                saving_data.loadData()
                temp_boid = int(saving_data.getBoardID())
                temp_pawn = int(saving_data.getPawn())
                self.setFromLoad(temp_boid,temp_pawn)

    def popUpMsg(self,message):
        '''
        We can print the message to the board or pop-up windows but not a chance we will print it on just terminal.
        '''
        print(message)

    def setFromLoad(self,boid,prev_pawn):
        self.board_id = boid
        self.pawn = prev_pawn

    def playListener(self):
        running = True
        popupbox=None
        popuptext=None
        self.drawbox("",20,"freesansbold.ttf",(255,255,255),(800),(100),350,200,(0,0,0),(150,150,150))
        while running:
            if self.current_board == None and self.board_id != -1:
                self.current_board = singleboard.SingleBoard(self.board_id)
                self.current_board.reJoin(self.pawn)
            self.updateBoard()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    seek=True
                    breakmaster=False
                    for y in range(9):
                        for x in range(9):
                            if self.button[str(x)+" "+str(y)].collidepoint(pos):
                                self.updateBoard()
                                if self.xo[x][y] == None:
                                    # nanti disini get ID boardnya idboard = self.boardstatus
                                    # ======================================================
                                    # 
                                    
                                    #Ini buat yang pertama kali join
                                    idboard=self.update_board_status(x,y)
                                    if self.pawn == 0:
                                        # print(idboard)
                                        self.current_board = singleboard.SingleBoard(idboard)
                                        self.pawn = self.current_board.joinGame(self.xo)
                                        self.board_id = idboard
                                        saving_data = player.Player()
                                        saving_data.setGameStatus('1')
                                        saving_data.setBoardID(str(self.board_id))
                                        saving_data.setPawn(str(self.pawn))
                                        saving_data.saveData()

                                    my_turn = self.current_board.isMyTurn(self.xo)
                                    # pieces = self.current_board.countPieces(self.xo)
                                    # print(pieces)
                                    # print(self.xo)

                                    if not my_turn:
                                        print('Bukan giliranmu bro')
                                    else:
                                        if self.current_board.getMyBoardID() == idboard:
                                            if self.pawn == 1:
                                                self.xo[x][y]=1
                                                print(self.xo)
                                                self.proxy.input(self.xo)
                                                # self.update_board_status(x,y)
                                                # self.createText("X","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)
                                            elif self.pawn == 2:
                                                self.xo[x][y]=2
                                                print(self.xo)
                                                self.proxy.input(self.xo)
                                                # print(self.xo)
                                                # self.createText("O","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)
                                            self.drawbox("",20,"freesansbold.ttf",(255,255,255),(800),(100),350,200,(0,0,0),(150,150,150))
                                        else:
                                            print("Jangan Klik Board Lain Bro")
                                else:
                                    temptext = threading.Thread(target=self.createTempText, args=(1,"Already Filled","freesansbold.ttf",50,(255,255,255),975,200))
                                    temptext.start()
                                    # self.createText("Already Filled","freesansbold.ttf",50,(255,255,255),975,200)
                                    # self.popUpMsg("Already Filled")
                                breakmaster=True
                                break
                        if breakmaster==True:
                            break            
            pygame.display.update()


def main():
    _player = player.Player()
    myBoard = TicTacToe()

    #Load Previous Data
    _player.loadData()
    is_played = _player.getGameStatus()
    if is_played == '1':
        temp_boid = int(_player.getBoardID())
        temp_pawn = int(_player.getPawn())

        myBoard.setFromLoad(temp_boid,temp_pawn)

    #Game Logic
    myBoard.createBoard()
    myBoard.playListener()

if __name__ == '__main__':
    main()