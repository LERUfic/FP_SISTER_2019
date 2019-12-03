import pygame

pygame.init()

screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption("Tic Tac Toe")
screen.fill((255,255,255))

xo=[[None for j in range(9)] for i in range(9)]
kotak=dict()
button=dict()
x0=350
y0=100
for x in range(9):
	x1=x0
	for y in range(9):
		loc=str(x)+','+str(y)
		#(a,b)=x1 x2 y1 y2
		coordinate=str(x1)+" "+str(x1+60)+" "+str(y0)+" "+str(y0+60) 
		kotak[loc]=coordinate
		button[str(x)+' '+str(y)]=pygame.draw.rect(screen, (176, 175, 178),(x1,y0,60,60))
		x1=x1+65
	y0=y0+65

pygame.display.update()

def text_objects(text,font,color):
	textSurface = font.render(text,True,color)
	return textSurface, textSurface.get_rect()

def createText(text,font,size,color,x,y):
	largeText = pygame.font.Font(font, size)
	TextSurf, TextRect = text_objects(text,largeText,color)
	TextRect.center=x,y
	screen.blit(TextSurf,TextRect)

running = True
while running:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pos = pygame.mouse.get_pos()
			seek=True
			breakmaster=False
			for x in range(9):
				for y in range(9):
					if button[str(x)+" "+str(y)].collidepoint(pos):
						print(button[str(x)+" "+str(y)])
						xo[x][y]=1
						print(xo)
						# X
						# createText("X","freesansbold.ttf",50,(0,0,0),int(button[str(x)+" "+str(y)][0])+30,float(button[str(x)+" "+str(y)][1])+32.5)
						
						# O
						createText("O","freesansbold.ttf",50,(0,0,0),int(button[str(x)+" "+str(y)][0])+30,float(button[str(x)+" "+str(y)][1])+32.5)
						
						# textRect.left= button[str(x)+" "+str(y)][0]
						# button[str(x)+' '+str(y)]=pygame.draw.rect(screen, (255, 0, 0),(button[str(x)+" "+str(y)][0],button[str(x)+" "+str(y)][1],60,60))
						breakmaster=True
						break
				if breakmaster==True:
					break
	pygame.display.update()
