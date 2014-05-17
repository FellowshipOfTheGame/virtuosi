#coding: utf-8
import pygame
from Button import *
import sys
def ler(tela,lang):
	btn_salvar = Button(0)
	btn_cancelar = Button(0)
	ct =0
	capslock =0
	b = ""
	aux = ''
	cursor_picture = pygame.image.load('Graphics/Mouse/Batuta.png').convert_alpha()
	fonte = pygame.font.Font("Data/Carolingia.ttf", 25)
	flag =0
	bkg = pygame.image.load("Graphics/Screens/Create.jpg")
	tela.blit(bkg,(0,0))
	tela.blit(fonte.render(("Create Profile:  "), False, (226, 157, 54) ),(0,0))
	pygame.display.flip()
	while (flag == 0):
		tela.blit(bkg,(0,0))
		tela.blit(fonte.render(("Create Profile:  "), False, (226, 157, 54) ),(0,0))
		for evento in pygame.event.get():
			if evento.type == pygame.MOUSEBUTTONUP:
				if Bleft == True:
					px , py = pygame.mouse.get_pos()
					#botao salvar
					if ((px>= 70)and (px<=270)) and ((py>= 510)and (py<=560)):
						flag = 1
						return (b)
					#botao cancelar
					if ((px>= 530)and (px<=730)) and ((py>= 510)and (py<=560)):
						flag = 1
						b = '#'
						btn_cancelar.click()
					Bleft == False
			if evento.type == pygame.MOUSEBUTTONDOWN:
				Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
			if evento.type == pygame.QUIT:
				sys.exit()
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE:
					flag = 1
					b = '#'
				if evento.key == pygame.K_RETURN:
					if (len(b) > 0):
						flag = 1
						return (b)
				# pega letras minusculas
				if (evento.key>= 97 and evento.key<=122):
					aux =chr(evento.key)
					ct = 1
				# pega letras maiusculas
				if (evento.key>= 65 and evento.key<=90):
					aux =chr(evento.key)
					ct = 1
				if evento.key == pygame.K_BACKSPACE:
					if (len(b) > 0):
						b = b[:-1]
			if (ct > 0):
				ct =0
				if (len(b) < 15):
					if (capslock == 1):
						b = b +aux.upper()
					else:
						b = b +aux
		#DESENHA O MOUSE
		tela.blit(cursor_picture, pygame.mouse.get_pos())
		tela.blit(fonte.render(b, False, (226, 157, 54) ),(265,300))
		#Desenha botoes
		tela.blit(btn_salvar.desenha(),(70,510))
		tela.blit(btn_cancelar.desenha(),(530,510))
		tela.blit(fonte.render(lang.Get(16), False, (226, 157, 54) ),(70,520))
		tela.blit(fonte.render(lang.Get(17), False, (226, 157, 54) ),(576,520))
		pygame.display.flip()
		if btn_salvar.getState() or btn_cancelar.getState():
				time.sleep(0.2)
	return (b)
#conta 2 "_" referente a Opus_x_[Nome]
def arruma_texto(texto):
	aux = 0
	for i in range(len(texto)):
		if texto[i] == "_":
			if aux < 1:
				aux +=1
			else:
				break
	aux = ((texto[i+1:].replace("_"," ")).title())
	return aux[:20]


gtela = None
glanguage = None
def Globais(ptela, planguage):
	global gtela
	global glanguage
	gtela = ptela
	glanguage = planguage

#tela de carregando
def Load(progress):
	global gtela, glanguage
	load = pygame.image.load("Graphics/Screens/Load.jpg")
	bar_cheio = pygame.image.load("Graphics/Boxes/LoadBar1.png")
	bar_vazio = pygame.image.load("Graphics/Boxes/LoadBar2.png")
	gtela.blit(load,(0,0))
	gtela.blit(pygame.font.Font("Data/Carolingia.ttf", 50).render((glanguage.Get(18)+"..."), False, (226, 157, 54) ), \
		(400-(pygame.font.Font("Data/Carolingia.ttf", 50).render((glanguage.Get(18)+"..."), False, (226, 157, 54) )).get_width()/2,200))
	gtela.blit(bar_cheio,(112,323))
	gtela.blit(pygame.transform.scale(bar_vazio ,(int (578*((100-progress)/100)), 36)),(688-576*((100-progress)/100),323))
	pygame.display.flip()

#testa achieviments
def testa_achie(nivel,miss,maxcombo,perform):
	print (repr(nivel)+"|"+repr(miss)+"|"+repr(maxcombo)+"|"+repr(perform))
	if nivel == 1:
		if perform > 89 and perform < 97:
			return 4
		elif perform >= 97:
			return 8
	elif nivel == 2:
		if perform > 89 and perform < 97:
			return 5
		elif perform >= 97:
			return 9
	elif nivel == 5:
		if perform > 89 and perform < 97:
			return 6
		elif perform >= 97:
			return 10
	elif nivel == 10:
		if perform > 89 and perform < 97:
			return 7
		elif perform >= 97:
			return 11
	return -1
