import pygame

pygame.init()

screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption("Tic Tac Toe")
screen.fill((255,255,255))

xo=[[None]*9]*9
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
myfont = pygame.font.SysFont('Comic Sans MS', 30)

pygame.display.update()

running = True
while running:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pos = pygame.mouse.get_pos()
			for x in range(9):
				for y in range(9):
					if button[str(x)+" "+str(y)].collidepoint(pos):
						print(button[str(x)+" "+str(y)])
						xo[x][y]=1
						print(xo)
						button[str(x)+' '+str(y)]=pygame.draw.rect(screen, (255, 0, 0),(button[str(x)+" "+str(y)][0],button[str(x)+" "+str(y)][1],60,60))
						break
	pygame.display.update()
