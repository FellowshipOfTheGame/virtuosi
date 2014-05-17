#coding: utf-8
import pygame
import threading
import time
import math
from Fret import *

jogando = True
parado = False
class Gameplay ( threading.Thread ) :
	#IMAGES
	frets = [None,None,None,None,None,None,None,None,None,None]
	sombra = 0
	tela = None
	bkg = None
	bar = None
	font = None
	arco_picture = None
	braco = None
	topo = None
	fundos = [None,None,None,None]
	selec = [None,None,None,None]
	
	#listas q conterão a partitura
	play_list = []
	pressing = []
	musica = ""
	
	#variaveis de jogo
	max_notas = 0
	notas_cont = 0
	max_cont = 0
	qtd_miss = 0
	points = 0
	multiplier = 1
	count = 0
	performance = 50
	nivel = 0
	audio = 1.0
	top = 0
	temp_top = 0
	language = None
	arco_pos = 1
	SP_meter = 0
	SP_active = False
	recomeca = False
	header_time = 0
	ms_by_mdc = 0
	tempo = None
	mstick = 0
	dif_enum = {1: 4, 2: 3, 5: 2, 10: 1}
	def __init__ (self, tela, language, music, musica, tempo, nivel=1, audio=1.0, header_time=0):
		self.frets[0] = pygame.image.load("Graphics/Frets/fret_green_full.png")
		self.frets[1] = pygame.image.load("Graphics/Frets/fret_red_full.png")
		self.frets[2] = pygame.image.load("Graphics/Frets/fret_yellow_full.png")
		self.frets[3] = pygame.image.load("Graphics/Frets/fret_blue_full.png")
		#Nota de SP
		self.frets[4] = pygame.image.load("Graphics/Frets/star_power.png")
		
		self.frets[5] = pygame.image.load("Graphics/Frets/f_1.png")
		self.frets[6] = pygame.image.load("Graphics/Frets/f_2.png")
		self.frets[7] = pygame.image.load("Graphics/Frets/f_3.png")
		self.frets[8] = pygame.image.load("Graphics/Frets/f_4.png")

		#efeito de nota na marca
		self.fundos[0] = pygame.image.load("Graphics/Frets/f_1.png")
		self.fundos[1] = pygame.image.load("Graphics/Frets/f_2.png")
		self.fundos[2] = pygame.image.load("Graphics/Frets/f_3.png")
		self.fundos[3] = pygame.image.load("Graphics/Frets/f_4.png")

		self.selec[0] = pygame.image.load("Graphics/Frets/fc_1.png")
		self.selec[1] = pygame.image.load("Graphics/Frets/fc_2.png")
		self.selec[2] = pygame.image.load("Graphics/Frets/fc_3.png")
		self.selec[3] = pygame.image.load("Graphics/Frets/fc_4.png")

		self.musica = musica
		self.pressing = [False,False,False,False]
		self.tela = tela
		self.language = language
		self.play_list = music
		self.header_time = header_time
		self.tempo = tempo
		self.audio = audio
		
		self.braco = pygame.image.load('Graphics/Screens/Braco.png').convert_alpha()
		self.arco_picture = pygame.image.load('Graphics/Mouse/Arco.png').convert_alpha()
		#recebe o nivel de dificuldade
		if (nivel == 1) or (nivel ==2) or (nivel ==5) or (nivel ==10):
			self.nivel = nivel
		else:
			self.nivel = 2

		# faz pre processaamento
		if self.play_list != None:
			self.pre_pro()

		#background e topground
		opus = musica.split('_')
		try:
			self.bkg = pygame.image.load("Data/Musics/Opus_"+opus[1]+".jpg")
		except:
			self.bkg = pygame.image.load("Graphics/Screens/bkg.jpg")
		#MOLDURA DO TOPO
		self.topo = pygame.image.load("Graphics/Screens/top.png").convert_alpha()
		#BARRA DE CARGA
		self.bar = pygame.image.load("Graphics/Others/bar.png")
		
		self.font = pygame.font.Font("Data/Carolingia.ttf", 16)
		#inicializa thread
		threading.Thread.__init__ ( self )

	#thread de jogo
	def run ( self ):
		global jogando
		global parado
		checkbox= pygame.image.load("Graphics/Boxes/Checked.jpg")
		#carregando musica
		pygame.mixer.init()
		pygame.mixer.music.load("Data/Musics/"+self.musica+".mid")
		pygame.mixer.music.set_volume (self.audio)
		ipf_control = 0
		#VARIÁVEIS DE GAMEPLAY
		playable = [False,False,False,False]
		miss = 0
		aux_cont = 0
		self.top = 0
		self.temp_top = 1
		gre = []
		red = []
		yel = []
		blu = []
		#agrpando lista de notas
		conjunto = [gre, red, yel, blu]
		clock = pygame.time.Clock()
		self.notas_cont =0
		self.max_cont = 0
		self.qtd_miss = 0
		self.points = 0
		self.multiplier = 1
		self.count = 0
		self.performance = 50
		#LOOP PRINCIPAL
		jogando = True
		pygame.mouse.set_pos([320,504])
		self.ms_by_mdc = self.tempo[0][1]/(self.header_time*1000)
		tic = 0
		syncing = True
		atraso = 0
		t = 0
		while jogando:
			playable[0] = False
			playable[1] = False
			playable[2] = False
			playable[3] = False
			miss = 0

			#ve se a fret na area tocavel
			#A REGIÃO DE ACERTO ESTÁ ENTRE 490 E 550
			if (len(gre) >0):
				if (gre[0].GetPy()>= 450) and (gre[0].GetPy()<= 550):
					playable[0] = True

			if (len(red) >0):
				if (red[0].GetPy()>= 450) and (red[0].GetPy()<= 550):
					playable[1] = True

			if (len(yel) >0):
				if (yel[0].GetPy()>= 450) and (yel[0].GetPy()<= 550):
					playable[2] = True

			if (len(blu) >0):
				if (blu[0].GetPy()>= 450) and (blu[0].GetPy()<= 550):
					playable[3] = True
			aux_cont = 0
			#CALCULAR ACERTO DE NOTAS
			#A REGIÃO DE ACERTO ESTÁ ENTRE 490 E 550
			if (len(gre) >0):
				if ((playable[0]) and (self.pressing[0])):
					#SE HOUVER NOTA VERDE TOCÁVEL E JOGADOR ESTÁ SEGURANDO A CASA
					if (gre[0].GetPy()>= 450) and (gre[0].GetPy()<= 550):
						pygame.mixer.music.set_volume(self.audio)
						aux_cont+=1
						self.pressing[0] = False
						if(self.SP_meter < 100):
							self.SP_meter += 1
						self.notas_cont += 1
						self.count += 1
						if (self.count % 20 == 0):
							if (self.multiplier != 10):
								self.multiplier += 1
						if gre[0].getTam() == 1:
							del gre[0]
						else:
							if gre[0].getTam() == 0:
								self.count += 1
								del gre[0]
						"""elif (gre[0].GetPy()< 450):
							self.pressing[0] = False"""
					else:
						self.pressing[0] = False
				else:
					self.pressing[0] = False
			if (len(red) >0):
				if ((playable[1]) and (self.pressing[1])):
					#SE HOUVER NOTA VERMELHA TOCÁVEL E JOGADOR ESTÁ SEGURANDO A CASA
					if (red[0].GetPy()>= 450) and (red[0].GetPy()<= 550):
						pygame.mixer.music.set_volume(self.audio)
						aux_cont+=1
						self.pressing[1] = False
						if(self.SP_meter < 100):
							self.SP_meter += 1
						self.notas_cont += 1
						self.count += 1
						if (self.count % 20 == 0):
							if (self.multiplier != 10):
								self.multiplier += 1
						if red[0].getTam() == 1:
							del red[0]
						else:
							if red[0].getTam() == 0:
								self.count += 1
								del red[0]
						"""elif (red[0].GetPy()< 450):
							self.pressing[1] = False"""
					else:
						self.pressing[1] = False
				else:
					self.pressing[0] = False
			if (len(yel) >0):
				if ((playable[2]) and (self.pressing[2])):
					#SE HOUVER NOTA AMARELA TOCÁVEL E JOGADOR ESTÁ SEGURANDO A CASA
					if (yel[0].GetPy()>= 450) and (yel[0].GetPy()<= 550):
						pygame.mixer.music.set_volume(self.audio)
						aux_cont+=1
						self.pressing[2] = False
						if(self.SP_meter < 100):
							self.SP_meter += 1
						self.notas_cont += 1
						self.count += 1
						if (self.count % 20 == 0):
							if (self.multiplier != 10):
								self.multiplier += 1
						if yel[0].getTam() == 1:
							del yel[0]
						else:
							if yel[0].getTam() == 0:
								self.count += 1
								del yel[0]
						"""elif (yel[0].GetPy()< 450):
							self.pressing[2] = False"""
					else:
						self.pressing[2] = False
				else:
					self.pressing[0] = False
			if (len(blu) >0):
				if ((playable[3]) and (self.pressing[3])):
					#SE HOUVER NOTA AZUL TOCÁVEL E JOGADOR ESTÁ SEGURANDO A CASA
					if (blu[0].GetPy()>= 450) and (blu[0].GetPy()<= 550):
						pygame.mixer.music.set_volume(self.audio)
						aux_cont+=1
						self.pressing[3] = False
						if(self.SP_meter < 100):
							self.SP_meter += 1
						self.notas_cont += 1
						self.count += 1
						if (self.count % 20 == 0):
							if (self.multiplier != 10):
								self.multiplier += 1
						if blu[0].getTam() == 1:
							del blu[0]
						else:
							if blu[0].getTam() == 0:
								self.count += 1
								del blu[0]
						"""elif (blu[0].GetPy()< 450):
							self.pressing[3] = False"""
					else:
						self.pressing[3] = False
				else:
					self.pressing[0] = False
			self.pressing = [False, False, False, False]
			if(self.SP_active):
				self.points += (2)*self.multiplier*aux_cont
			else:
				self.points += (1)*self.multiplier*aux_cont
			if self.count > self.max_cont:
				self.max_cont = self.count
			#LOGICA DO STAR POWER
			if(self.SP_active):
				self.SP_meter -= 0.05
				if(self.SP_meter <= 0):
					self.SP_active = False
					self.SP_meter = 0
			
			#SE VIER NOVAS NOTAS NA TELA
			#CRIAR NOTAS NO SELF.TOPO
			if self.play_list != None:
				if len(self.play_list) > 0:
					if len(self.tempo) > 0 and self.temp_top < len(self.tempo):
						if (self.tempo[self.temp_top][0]*(self.ms_by_mdc)) <= tic:
							temp = self.tempo[self.temp_top][1]/(self.header_time*1000)
							#temp = self.tempo[self.temp_top][1]/(self.header_time*1000)
							#print("O Tic antes e :" + repr(tic))
							tic = self.tempo[self.temp_top][0]*(temp)
							
							if temp < self.ms_by_mdc:
								tic -= self.header_time
							#	atraso = (self.play_list[self.top][0]*(self.ms_by_mdc))
							#	tic = 0
								#153855   15234
								#tic -= (self.ms_by_mdc - temp)/self.header_time
								#tic -= self.play_list[self.top][0]*((self.ms_by_mdc - temp)/self.header_time)
								#tic -= (self.ms_by_mdc - temp)*1000
							elif temp > self.ms_by_mdc:
								tic += self.header_time
							self.ms_by_mdc = temp
							
							print("O Tic depois e :" + repr(tic))
							print("O coeficiente novo e " + repr(self.ms_by_mdc))
							print("O tempo Mudou para " + repr(self.tempo[self.temp_top][1]))
							self.temp_top += 1
							#tic += atraso
							#print ("atraso total:"+repr(atraso))
							#atraso = 0
						
					tic += clock.tick()
					self.t = 0
					#print( repr(self.play_list[self.top][0]) + " -- " + repr(self.play_list[self.top][0]*(self.ms_by_mdc)) + " -- " + repr(tic))
					while self.top < len(self.play_list) and((self.play_list[self.top][0]*(self.ms_by_mdc)) <= tic):
						qtd_t = 0
						#print (repr((self.play_list[self.top][0]*(self.ms_by_mdc)-atraso)) + " -- " + repr(tic))
						#atraso += (2000 - tic) - self.play_list[self.top][0]*(self.ms_by_mdc)
						#PULA NOTAS ATRASADAS
						if (self.top < len(self.play_list)):
							while ((self.play_list[self.top][0]*(self.ms_by_mdc)) <= tic):
								self.top+=1
								if self.top >= len(self.play_list):
									break
						if self.top >= len(self.play_list):
									break
						"""if self.play_list[self.top][2] != 0:
							qtd_t += self.aux(self.play_list[self.top][2],self.play_list[self.top][0])
							if qtd_t >2:
								conjunto[self.play_list[self.top][1] %4].append(Fret(self.play_list[self.top][1] %4,2,qtd_t))
							else:
								conjunto[self.play_list[self.top][1] %4].append(Fret(self.play_list[self.top][1] %4))
						else:"""
						conjunto[self.play_list[self.top][1] %4].append(Fret(self.play_list[self.top][1] %4))
						
						if self.t == 3:
							print("Imprimiu 4 notas em MidiClks: " + repr(self.play_list[self.top][0]))
						
						self.t += 1
						self.top += 1
						if self.top >= len(self.play_list):
							print("Passou do ponto...")
							break
					
			if syncing:
				if tic >= 2000:
					pygame.mixer.music.play()
					print("FUCK -- " + repr(tic))
					syncing = False
							
			# Apaga frets q sairam da tela
			if (len(gre)>0) :
				if (gre[0].GetPy() >= 600):
					miss += 1*(2-gre[0].GetTipo())
					del gre[0]
			if (len(red)>0):
				if (red[0].GetPy() >= 600):
					miss += 1*(2-red[0].GetTipo())
					del red[0]
			if (len(yel)>0):
				if (yel[0].GetPy() >= 600):
					miss += 1*(2-yel[0].GetTipo())
					del yel[0]
			if (len(blu)>0):
				if (blu[0].GetPy() >= 600):
					miss += 1*(2-blu[0].GetTipo())
					del blu[0]
					
			#calcula performace
			if self.notas_cont > 0:
				self.performance = int (100*(self.notas_cont - self.qtd_miss)/self.notas_cont)
				if self.performance< 0:
					self.performance = 0
			#se errou alguma tecla
			if (miss != 0):
				#pausa a musica
				pygame.mixer.music.set_volume(0.0)
				self.multiplier = 1
				self.qtd_miss += miss
				self.count = 0
			#acha a maior lista de notas
			#qtd de maior utilizado a seguir
			qtd_listas = [len(gre), len(red),len(yel),len(blu)]
			qtd_listas.sort()
			maior = qtd_listas[3]

			ipf_control+=1
			if (ipf_control == 10):
				ipf_control = 0
				#ATUALIZAR ESTADOS DA TELA
				#REDESENHAR O MARCADOR DE DESEMPENHO(SE NECESSÁRIO)
				self.tela.blit(pygame.transform.scale(self.bkg, (800, 600)),(0,0))
				self.tela.blit(self.braco,(125,0))
				if (self.arco_pos == 0):
					self.tela.blit(self.selec[0],(143,484))
				if (self.arco_pos == 0) or (self.arco_pos == 1):
					self.tela.blit(self.selec[1],(242,474))
				if (self.arco_pos == 1) or (self.arco_pos == 2):
					self.tela.blit(self.selec[2],(343,474))
				if (self.arco_pos == 2):
					self.tela.blit(self.selec[3],(443,484))
				# DESENHA FUNDO DA AREA DE CLIQUE
				#ATUALIZAR POSIÇÃO DAS NOTAS
				#SE A NOTA EXISTE MOVE A NOTA E REDIMENSIONA
				#E
				#DESENHA FRETS
				for i in range(maior):
					#NOTAS VERDES
					if i < len(gre):
						sombra = 0
						gre[i].Move()
						if (gre[0].GetPy()>= 470) and (gre[0].GetPy()<= 550):
							sombra =  1
						self.tela.blit(pygame.transform.scale(self.frets[4*(self.SP_active)+sombra*5*(1-self.SP_active)] ,(gre[i].GetTw(), gre[i].GetTh())),(gre[i].GetPx(),gre[i].GetDrawPy()))
					#NOTAS VERMELHAS
					if i < len(red):
						sombra = 0
						red[i].Move()
						if (red[0].GetPy()>= 470) and (red[0].GetPy()<= 550):
							sombra =  1
						self.tela.blit(pygame.transform.scale(self.frets[1+3*(self.SP_active)+sombra*5*(1-self.SP_active)] ,(red[i].GetTw(), red[i].GetTh())),(red[i].GetPx(),red[i].GetDrawPy()))
					#NOTAS AMARELAS
					if i < len(yel):
						sombra = 0
						yel[i].Move()
						if (yel[0].GetPy()>= 470) and (yel[0].GetPy()<= 550):
							sombra =  1
						self.tela.blit(pygame.transform.scale(self.frets[2+2*(self.SP_active)+sombra*5*(1-self.SP_active)] ,(yel[i].GetTw(), yel[i].GetTh())),(yel[i].GetPx(),yel[i].GetDrawPy()))
					#NOTAS AZUIS
					if i < len(blu):
						sombra = 0
						blu[i].Move()
						if (blu[0].GetPy()>= 470) and (blu[0].GetPy()<= 550):
							sombra =  1
						self.tela.blit(pygame.transform.scale(self.frets[3+1*(self.SP_active)+sombra*5*(1-self.SP_active)] ,(blu[i].GetTw(), blu[i].GetTh())),(blu[i].GetPx(),blu[i].GetDrawPy()))
				#ATUALIZAR MODIFICADOR DE PONTOS
				#ATUALIZAR OS PONTOS
				#REDESENHAR TUTÔ
				#DESENHANDO FORMAS FIXAS
				#O CENTRO DA BORDA SUPERIOR É (320,0)
				#CADA PISTA DISTA 15 PIXELS NO TOPO E 90 PIXELS NA BASE
				#pygame.draw.line(self.tela,(226, 157, 54),(315,-1),(125,600),2)  #BORDA ESQUERDA
				#pygame.draw.line(self.tela,(226, 157, 54),(375,-1),(575, 600),2)  #BORDA DIREITA
				
				#ÁREA DE TOCAR NOTAS
				#pygame.draw.line(self.tela,(226, 157, 54),(330,-1),(255,600),2)
				#pygame.draw.line(self.tela,(226, 157, 54),(345,-1),(345,600),2)
				#pygame.draw.line(self.tela,(226, 157, 54),(360,-1),(435,600),2)
				#Retas das notas
				#pygame.draw.line(self.tela,(0,255,0),(295,-1),(165,600),2)
				#pygame.draw.line(self.tela,(0,255,0),(312,-1),(275,600),2)
				#pygame.draw.line(self.tela,(0,255,0),(327,-1),(365,600),2)
				#pygame.draw.line(self.tela,(0,255,0),(342,-1),(480,600),2)
				#linha horizontais
				pygame.draw.line(self.tela,(226, 157, 54),(158,470),(535,470),2)
				pygame.draw.line(self.tela,(226, 157, 54),(150,520),(550,520),2)
				self.tela.blit(self.font.render(("A"), False, (226, 157, 54) ),(190,494))
				self.tela.blit(self.font.render(("S"), False, (226, 157, 54) ),(300,494))
				self.tela.blit(self.font.render(("D"), False, (226, 157, 54) ),(375,494))
				self.tela.blit(self.font.render(("F"), False, (226, 157, 54) ),(463,494))
				#PLACAR
				self.tela.blit(pygame.transform.scale(self.bar ,(59, math.trunc(self.SP_meter))),(736,math.trunc(100-self.SP_meter)))
				#print(self.SP_meter)
				self.tela.blit(pygame.transform.scale(self.bar ,(59, self.performance)),(10,100-self.performance))
				self.tela.blit(self.topo,(0,0))
				self.tela.blit(self.font.render(("Perform:"+repr(self.performance)), False, (0, 0, 0) ),(0,0))
				self.tela.blit(self.font.render(("X"+repr(self.multiplier)), False, (0, 0, 0) ),(400,50))
				
				self.tela.blit(self.font.render(("Pontos "+repr(self.points)), False, (0, 0, 0) ),(150,10))
				self.tela.blit(self.font.render(("Combo: "+repr(self.count)+"/"+repr(self.max_cont)), False, (0, 0, 0) ),(500,10))
				self.tela.blit(self.font.render(("qtd miss "+repr(self.qtd_miss)), False, (0, 0, 0) ),(350,10))
				"""for ax in range(-11,10):
					for dax in range (10):
						pygame.draw.line(self.tela, (0,255,0), (345+(ax+dax/10)*18,470-(20-math.pow((ax+dax/10),4)/1024)), (345+(1+ax+dax/10)*18,470-(20-math.pow((1+ax+dax/10),4)/1024)),2)
						pygame.draw.line(self.tela, (0,255,0), (345+(ax+dax/10)*18,510-(5-math.pow((ax+dax/10),4)/1024)), (345+(1+ax+dax/10)*18,510-(5-math.pow((1+ax+dax/10),4)/1024)),2)"""

				#DESENHA O MOUSE
				# y - y0 = y'x -y'x0
				#y = y'x +(y0 -y'x0)
				#angle = y'/(y0 - y'x0)
				px, py = pygame.mouse.get_pos()
				x0 = math.trunc(px/18)-17
				y0 = 20-(math.pow(x0,4)/1024)
				#print (y0)
				yl = -(math.pow(x0,3)/256)
				#print (yl)
				#print(repr(x0)+"|"+repr(y0))
				angle = (yl /(y0 - yl*x0))
				angle = angle
				angle = math.degrees(angle)
				self.tela.blit(pygame.transform.rotate(self.arco_picture,angle),(px-318, 410-math.asin(math.radians(angle))))
				pygame.display.flip()

			#inicio tela de pause
			while (parado == True):
				pass
				#pygame.mixer.music.pause()
				#reseta variaveis
			if self.recomeca == True:
				playable = [False,False,False,False]
				miss = 0
				gre = []
				red = []
				blu = []
				yel = []
				self.notas_cont =0
				self.max_cont = 0
				self.qtd_miss = 0
				self.points = 0
				self.multiplier = 1
				self.count = 0
				self.performance = 50
				self.top = 0
				self.temp_top = 0
				tic = clock.tick()
				tic = clock.tick()
				self.recomeca = False
			if (pygame.mixer.music.get_busy() == False and tic >= 20000):
				print ("fim da musica")
				jogando = False
	#preprocessamento
	def pre_pro(self):
		second_octave = 0
		note_number = 0
		past_number = 0
		i = 0
		j = 0
		color = 0
		past_color = -1
		#Remove notas proximas de acordo com dificuldade
		for i in range(len(self.play_list)-2):
			if i > len(self.play_list)-2:
				break
			for j in range(1,10):
				if i+j < len(self.play_list)-2:
					if (self.play_list[i][0]+self.dif_enum[self.nivel]*self.header_time) > self.play_list[i+j][0]:
						self.play_list.pop(i+j)
		for i in range(len(self.play_list)):
			note_number = self.play_list[i][1]
			if i != 0:
				past_color = color
			color = note_number % 4
			#se a nota anterior for verde
			if past_color == 0:
				if color == 3:
					#print (repr(i)+"de azul para para vermelho")
					self.play_list[i][1] -= 2
				elif (color == 2):
					#print (repr(i)+"de amarelo para vermelho")
					self.play_list[i][1] -= 1
			#se a nota anterior for azul
			if past_color == 3:
				if color == 0:
					#print (repr(i)+"de verde para amarelo")
					self.play_list[i][1] += 2
				elif (color == 1):
					#print (repr(i)+"de vermelho para amarelo")
					self.play_list[i][1] += 1
		#encontra quantidade de notas
		#descobre quantos frets existem na musica
		if self.play_list != None:
			self.max_notas = len(self.play_list)

	#descobre a pontuacao media
	def Get_Pontucao_min(self):
		mult = self.max_notas/20
		pont = 0
		for i in range(mult+1):
			pont = pont + mult*20
		return (pont*0.5)
	def aux(self, fim, ini):
		temp = (fim - ini)/self.header_time
		return math.trunc(temp)
	#nao necessita de explicacao
	def Pauser(self):
		global parado
		global jogando
		itens =[]
		y = 0
		selected = pygame.image.load("Graphics/Buttons/botao.jpg")
		bkg = pygame.image.load("Graphics/Screens/Background.jpg")
		Carolingia_25 = pygame.font.Font("Data/Carolingia.ttf", 25)
		cursor_picture = pygame.image.load('Graphics/Mouse/Batuta.png').convert_alpha()
		#PREPARA PARA ESCREVER
		#itens.append (Carolingia_25.render(self.language.Get(20), False, (226, 157, 54) ))
		itens.append (Carolingia_25.render(self.language.Get(21), False, (226, 157, 54) ))
		itens.append (Carolingia_25.render(self.language.Get(9), False, (226, 157, 54) ))
		tam = len(itens)
		sair = False
		#onde_parou = pygame.mixer.music.get_pos()
		#pygame.mixer.music.stop()
		pygame.mixer.music.pause()
		while (sair == False):
			#DESENHA FUNDO
			self.tela.blit(bkg,(0,0))
			#DESENHA CAIXA DE SELECIONADO
			self.tela.blit(pygame.transform.scale(selected ,(250, 30)),(290,285))
			#DESENHA OPCOES
			self.tela.blit(itens[(y-1)%tam],(300,205)) #1
			self.tela.blit(itens[y],(300,290)) #2
			self.tela.blit(itens[(y+1)%tam],(300,370)) #3
			#DESENHA O MOUSE
			self.tela.blit(cursor_picture, pygame.mouse.get_pos())
			#PEGA EVENTOS
			for evento in pygame.event.get():
				#EVENTOS DO MOUSE
				if evento.type == pygame.MOUSEBUTTONUP:
					if Bleft == True:
						px , py = pygame.mouse.get_pos()
						if ((px>= 290)and (px<=540)) and ((py>= 285)and (py<=315)):
							sair = True
						if (py< 285):
							y -= 1
							if y < 0:
								y = tam-1
						if (py>315):
							y += 1
							if y > tam-1:
								y = 0
						Bleft == False
				if evento.type == pygame.MOUSEBUTTONDOWN:
					Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
				#EVENTOS DO TECLADO
				if evento.type == pygame.QUIT:
					sair = True
				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_RETURN:
						sair = True
					if evento.key == pygame.K_ESCAPE:
						parado = False
						return False
					if evento.key == pygame.K_DOWN:
						y += 1
						if y > len(itens)-1:
							y = 0
					if evento.key == pygame.K_UP:
						y -= 1
						if y < 0:
							y = len(itens)-1
					if evento.type == pygame.QUIT:
						rodando = False
			#ATUALIZA A TELA
			pygame.display.flip()
		pygame.mouse.set_pos([320,504])
		print (y)
		"""if (y == 0):
			#pygame.mixer.unpause()
			pygame.mixer..music.unpause()
			parado = False
		"""
		#elif (y==0):
		if (y==0):
			#pygame.mixer.music.rewind()
			pygame.mixer.music.stop()
			self.top = 0
			self.temp_top = 0
			self.points =self.qtd_miss=self.max_cont= self.performance=0
			parado = False
			self.recomeca = True
		elif (y==1):
			#pygame.mixer.stop()
			pygame.mixer.music.stop()
			self.points =self.qtd_miss=self.max_cont= self.performance=0
			jogando = False
			parado = False
			
	#função que inicia o jogo
	def Play(self):
		global jogando
		global parado
		jogando = True
		self.start()
		# loop para segurar o jogo dentro do gameplay
		cheat = 0
		px = py =0

		fps_control = 0
		while jogando:
			if parado == False:
				Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
				fps_control +=1
				if (fps_control == 2):
					fps_control = 0
					px, py = pygame.mouse.get_pos()
					if (px < 135):
						pygame.mouse.set_pos([135,504])
					if (px>525):
						pygame.mouse.set_pos([525,504])
					if (px  <= 275):
						self.arco_pos = 0
					elif ((px > 275) and (px< 375)):
						self.arco_pos = 1
					else:
						self.arco_pos = 2
				if (cheat == 5):
					self.pressing[0] = True
					self.pressing[1] = True
					self.pressing[2] = True
					self.pressing[3] = True
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						jogando = False
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							if (parado == True):
								parado = False
							else:
								parado = True
						#teste de cheat mode
						if (event.key == pygame.K_1):
							cheat += 1
							if cheat == 5:
								print ("Cheat on")
							if cheat >= 6:
								cheat = 0
								print ("Cheat off")
						#TESTES PARA CADA NOTA
						if (event.key == pygame.K_LEFT):
							if (self.arco_pos > 0):
								self.arco_pos -= 1
							pygame.mouse.set_pos([225+self.arco_pos*100,504])
						if (event.key == pygame.K_RIGHT):
							if (self.arco_pos < 2):
								self.arco_pos += 1
							pygame.mouse.set_pos([225+self.arco_pos*100,504])
						if event.key == pygame.K_SPACE:
							if(self.SP_meter >= 30):
								self.SP_active = True
						if (self.arco_pos == 0):
							if (event.key == pygame.K_a):
								self.pressing[0] = True
						if (self.arco_pos == 0) or (self.arco_pos == 1):
							if (event.key == pygame.K_s):
								self.pressing[1] = True
						if (self.arco_pos == 1) or (self.arco_pos == 2):
							if (event.key == pygame.K_d):
								self.pressing[2] = True
						if (self.arco_pos == 2):
							if (event.key == pygame.K_f):
								self.pressing[3] = True
						Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
				#TESTES DO STAR POWER
				if Bleft == True:
					if(self.SP_meter >= 30):
						self.SP_active = True
					Bleft == False

			else:
				self.Pauser()
		#pygame.mixer.music.stop()
		#pygame.mixer.quit()
		return int(self.points), self.qtd_miss, self.max_cont, self.performance