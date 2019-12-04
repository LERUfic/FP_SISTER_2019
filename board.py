import pygame
import threading
import time
pygame.init()

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

    def createBoard(self):
        for x in range(9):
            x1=self.x0
            for y in range(9):
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
        while i<5:
            print(i)
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

    def getLatestBoard(self):
        '''
        This is for testing purpose only.
        The actual getLatestBoard will be pulling data from server using Pyro4,
        then that data will be decode because probably we will use pickle as object serialization then return it.
        '''
        testing_board=[[None for j in range(9)] for i in range(9)]
        testing_board[1][1] = 1
        testing_board[4][2] = 1
        testing_board[6][3] = 1
        testing_board[1][4] = 1
        testing_board[2][8] = 1

        testing_board[8][5] = 2
        testing_board[7][6] = 2
        testing_board[1][7] = 2
        testing_board[1][2] = 2
        testing_board[4][3] = 2

        return testing_board

    def updateBoard(self):
        self.xo = self.getLatestBoard()

        for x in range(9):
            for y in range(9):
                if self.xo[x][y] == 1:
                    self.createText("X","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)
                elif self.xo[x][y] == 2:
                    self.createText("O","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)

        pygame.display.update()

    def popUpMsg(self,message):
        '''
        We can print the message to the board or pop-up windows but not a chance we will print it on just terminal.
        '''
        print(message)

    def playListener(self, pawn):
        running = True
        popupbox=None
        popuptext=None
        self.drawbox("",20,"freesansbold.ttf",(255,255,255),(800),(100),350,200,(0,0,0),(150,150,150))
        while running:
            self.updateBoard()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    seek=True
                    breakmaster=False
                    for x in range(9):
                        for y in range(9):
                            if self.button[str(x)+" "+str(y)].collidepoint(pos):
                                self.updateBoard()
                                if self.xo[x][y] == None:
                                    if pawn == 1:
                                        print(self.xo)
                                        self.xo[x][y]=1
                                        self.createText("X","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)
                                    elif pawn == 2:
                                        self.xo[x][y]=2
                                        self.createText("O","freesansbold.ttf",50,(0,0,0),int(self.button[str(x)+" "+str(y)][0])+30,float(self.button[str(x)+" "+str(y)][1])+32.5)
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
    myBoard = TicTacToe()
    myBoard.createBoard()
    myBoard.playListener(1)

if __name__ == '__main__':
    main()