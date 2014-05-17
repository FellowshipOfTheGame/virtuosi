#coding: utf-8
import pygame
import Extras
from Profiles import *
from Musics import *
from Gameplay import *
from Extras import *
from High_Score import *
from Config import *
from Languages import *
from Button import *
import sys
#todas as constants terao prefixo Const_
Const_default_y = 300

class Virtuosi:
	global Const_default_y
	config = None
	prof = None
	profile = None
	High_S = None
	lang = None
	languages = None
	opt = 0
	Carolingia_25 = None
	Carolingia_20 = None
	Old_English_25 = None
	cursor_picture= None 
	tela = None
	Achie = None
	def __init__ (self,tela):
		self.tela = tela
		#PREPARAÇÃO DA FONTE
		self.Carolingia_25 = pygame.font.Font("Data/Carolingia.ttf", 25)
		self.Carolingia_20 = pygame.font.Font("Data/Carolingia.ttf", 20)
		
		self.Old_English_25 = pygame.font.Font("Data/Old_English.ttf", 25)
		#carrega imagem do cursor
		self.cursor_picture = pygame.image.load('Graphics/Mouse/Batuta.png').convert_alpha()
		#carrega high score global
		self.High_S = High_Score()
		#carregando linguagem
		self.languages = Language("Portugues Brasileiro")
		self.lang = Lang (self.languages.GetOne())
		
		#adiciona tela e linguagem a var globais
		Globais(self.tela, self.lang)
		
		#tenta carregar um profile
		try:
			self.prof = Profiles()
			self.prof.Load()
			self.ChangeProf(1)
			#self.opt = 2
		except IOError:
			self.Create_profile()
			#self.opt = 1# faz com que vá para a tela de criar profile
	#MENU DE PROFILES
	def ChangeProf(self, param):
		itens =[]
		y = 0
		bkg = pygame.image.load("Graphics/Screens/Background.jpg")
		selected = pygame.image.load("Graphics/Buttons/botao.jpg")
		#PEGA LISTA DE PROFILES
		profiles_list = self.prof.GetList()
		#PREPARA PARA ESCREVER
		for i in profiles_list:
			#SE NECESSARIO RETIRA O '\N'
			aux = i
			aux = aux.replace("\n", "")
			itens.append(self.Carolingia_25.render(str(aux), False, (226, 157, 54) ))
		
		itens.append(self.Carolingia_25.render(self.lang.Get(0), False, (226, 157, 54) ))
		# se 1 = cancelar
		# se 9 = sair
		if param == 0:
			itens.append(self.Carolingia_25.render(self.lang.Get(1), False, (226, 157, 54) ))
		else:
			itens.append(self.Carolingia_25.render(self.lang.Get(9), False, (226, 157, 54) ))
		#var logica que verifica se o usuario quer apagar um profile
		rmv = 0
		tam = len(itens)
		while True:
			sair = False
			while (sair == False):
				#PEGA EVENTOS
				for evento in pygame.event.get():
					#EVENTOS DO MOUSE
					if evento.type == pygame.MOUSEBUTTONUP:
						if Bleft == True:
							px , py = pygame.mouse.get_pos()
							if ((px>= 400-selected.get_width()/2)and (px<=(400-selected.get_width()/2)+selected.get_width())) and ((py>= 290)and (py<=310)):
								sair = True
							if (py< 290):
								y -= 1
								if y < 0:
									y = tam-1
							if (py>310):
								y += 1
								if y > tam-1:
									y = 0
							Bleft == False
					if evento.type == pygame.MOUSEBUTTONDOWN:
						Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
					if evento.type == pygame.QUIT:
						sys.exit(0)
					#EVENTOS DO TECLADO
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_RETURN:
							sair = True
						#---------------------------------
						if evento.key == pygame.K_ESCAPE:
							rodando = False
						#---------------------------------
						#if evento.key == pygame.K_SPACE:
						#	sair = True
						#---------------------------------
						if evento.key == pygame.K_LEFT:
							if rmv == 1:
								rmv = 0
						#---------------------------------
						if evento.key == pygame.K_RIGHT:
							if (y >= 0) and (y<= tam -3):
								if param == 0:
									if (profiles_list[y] != self.profile.nome):
										if rmv == 0:
											rmv = 1
						#---------------------------------
						if evento.key == pygame.K_DOWN:
							rmv = 0
							y += 1
							if y > tam-1:
								y = 0
						#---------------------------------
						if evento.key == pygame.K_UP:
							rmv = 0
							y -= 1
							if y < 0:
								y = tam-1
						#---------------------------------
						if evento.type == pygame.QUIT:
							rodando = False
				#DESENHA FUNDO
				self.tela.blit(bkg,(0,0))
				#self.tela.blit(self.Carolingia_25.render(("Change Profile:  "+repr(y)), False, (226, 157, 54) ),(0,0))
				#self.tela.blit(itens[y],(0,0))
				#DESENHA CAIXA DE SELECIONADO
				self.tela.blit(pygame.transform.scale(selected ,(250, 30)),(400-selected.get_width()/2,285))
				#DESENHA OPCOES
				if (tam > 3):
					self.tela.blit(itens[(y-2)%tam],(400-(itens[(y-2)%tam].get_width()/2),150)) #1
				self.tela.blit(itens[(y-1)%tam],(400-(itens[(y-1)%tam].get_width()/2),205)) #2
				self.tela.blit(itens[y],(400-(itens[(y)%tam].get_width()/2),290)) #3
				self.tela.blit(itens[(y+1)%tam],(400-(itens[(y+1)%tam].get_width()/2),370)) #4
				if (tam > 4):
					self.tela.blit(itens[(y+2)%tam],(400-(itens[(y+2)%tam].get_width()/2),427)) #5
				if rmv == 1:
					self.tela.blit(self.Carolingia_25.render((self.lang.Get(2)+" ?"), False, (226, 157, 54) ),(400,290))
				#DESENHA O MOUSE
				self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
				#ATUALIZA A TELA
				pygame.display.flip()
			#chega e excecuta opcao selecionada
			if (y >= 0) and (y<= tam -3):
				if rmv == 1:
					self.prof.RmvOne(profiles_list[y])
					itens =[]
					profiles_list = self.prof.GetList()
					for i in profiles_list:
						aux = i
						if aux[-1] == "\n":
							aux = aux[:-1]
						itens.append(self.Carolingia_25.render(str(aux), False, (226, 157, 54) ))
					itens.append(self.Carolingia_25.render(self.lang.Get(0), False, (226, 157, 54) ))
					itens.append(self.Carolingia_25.render(self.lang.Get(1), False, (226, 157, 54) ))
					tam = len(itens)
					sair = False
					rmv = 0
				else:
					self.profile = Profile (profiles_list[y])
					self.prof.MoveUp(profiles_list[y])
					#self.opt = 3
					return False
			else:
				if y == (tam - 2): #chama tela de criação de profile
					if (self.Create_profile() == 0):
						self.profile = Profile (self.prof.GetOne())
						return False
					#self.opt = 1
				else:
					if param == 1:
						sys.exit(0)
					elif y == (tam-1):
						#self.opt = 3
						return False
	#CRIA PROFILE
	def Create_profile(self):
		sair = False
		nome_aux = ""
		while nome_aux == "":
			nome_aux = ler(self.tela,self.lang)
			if (nome_aux != '#'):
				self.prof.AddOne(nome_aux)
				self.prof.Save()
				self.profile = Profile (self.prof.GetOne())
				return 0
			else:
				nome_aux = ""
				if len(self.prof.GetList()) > 0:
					return 1
	#MENU PRINCIPAL
	def Menu_P(self):
		itens =[]
		y = 0
		selected = pygame.image.load("Graphics/Buttons/botao.jpg")
		bkg = pygame.image.load("Graphics/Screens/Background.jpg")
		#PREPARA PARA ESCREVER
		while True:
			del itens
			itens = []
			"""while self.opt != 3 :
				#se existe ao menos um chama mudanca
				#chamada padrao para criacao de novo profile
				if (self.opt == 0):
					self.ChangeProf(0)
					if self.opt == 0:
						self.opt = 3
				#se nao existe, cria um profile
				if (self.opt == 1):
					print ("cria profile")
					self.Create_profile()
					self.opt = 3
				#chamada obrigatoria para criacao de profile
				if (self.opt == 2):
					self.ChangeProf(1)"""
			#self.profile = Profile(self.prof.GetOne())
			#carrega configuracao
			self.config = self.profile.Return_Config()
			# carrega achieviments
			self.Achie = self.profile.Return_Achie()
			#testa fullscreen
			if self.config.Get_full() == 1:
				tela = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
			else:
				tela = pygame.display.set_mode((800, 600))
				
			#joga linguagem do profile para o topo
			self.languages.MoveUp(self.config.Get_lang())
			#carregando linguagem
			self.lang = Lang (self.languages.GetOne())
			Globais(self.tela, self.lang)
			
			for i in range(3,10):
				itens.append (self.Carolingia_25.render(self.lang.Get(i), False, (226, 157, 54) ))
			tam = len(itens)
			
			sair = False
			while (sair == False):
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
						sys.exit()
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_RETURN:
							sair = True
						if evento.key == pygame.K_ESCAPE:
							rodando = False
						if evento.key == pygame.K_SPACE:
							sair = True
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
				#DESENHA FUNDO
				self.tela.blit(bkg,(0,0))
				#self.tela.blit(self.Carolingia_25.render(("Menu Principal:  "+repr(y)), False, (226, 157, 54) ),(0,0))
				#DESENHA CAIXA DE SELECIONADO
				self.tela.blit(pygame.transform.scale(selected ,(250, 30)),(290,285))
				#DESENHA OPCOES
				self.tela.blit(itens[(y-2)%tam],(400-itens[(y-2)%tam].get_width()/2,150)) #1
				self.tela.blit(itens[(y-1)%tam],(400-itens[(y-1)%tam].get_width()/2,205)) #2
				self.tela.blit(itens[y],(400-itens[(y)%tam].get_width()/2,290)) #3
				self.tela.blit(itens[(y+1)%tam],(400-itens[(y+1)%tam].get_width()/2,370)) #4
				self.tela.blit(itens[(y+2)%tam],(400-itens[(y+2)%tam].get_width()/2,427)) #5
				#DESENHA O MOUSE
				self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
				#ATUALIZA A TELA
				pygame.display.flip()
			if (y == 0):
				self.Menu_V()
				# BE A VIRTUOSO
			elif (y==1):
				self.Menu_Q()
				# QUICK PLAY
			elif (y==2):
				self.Menu_H()
				# HIGH SCORE
			elif (y==3):
				self.Menu_A()
				# ACHIVMENT
			elif (y==4):
				self.ChangeProf(0)
				#self.opt = 0
				# ACHIVMENT
			elif (y==5):
				self.Option()
				# ACHIVMENT
			else:
				self.profile.save()
				return False
	#MENU DE CAMPANHA
	def Menu_V(self):
		Msc = Musics()
		btn_jogar = Button(0)
		btn_voltar = Button(0)
		btn_red_e = Button(1)
		btn_red_d = Button(1)
		btn_list_text = []
		btn_list_text.append(self.Old_English_25.render(self.lang.Get(19), False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render(self.lang.Get(1), False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render("<", False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render(">", False, (226, 157, 54) ))
		bkg = pygame.image.load("Graphics/Screens/Be_a_virtuoso.jpg")
		selected = pygame.image.load("Graphics/Boxes/Selected.jpg")
		unselected = pygame.image.load("Graphics/Boxes/Unselected.jpg")
		qtd = 0
		pag_atual = 0
		lado = 0
		msc_atual = 0
		aux = 0
		limit = 0
		
		list,qtd = Msc.GetList()
		esq = []
		dir = []
		tam = qtd[pag_atual]
		voltar = False
		score_aux =score_number = 0
		ajuda = False
		#LACO DO MENU 1
		while (voltar == False):
			esq = []
			dir = []
			#CALCULA QUAIS PAGINAS MOSTRAR
			if pag_atual < len(qtd):
				if pag_atual == 0:
					score_number= i = 0
					limit =qtd[pag_atual]
				else:
					score_number =i = qtd[pag_atual-1]
				while i < qtd[pag_atual]:
					if (i == 0):
						esq.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					elif (((self.profile.Get_V()[i-1])[2]) >= 50):
						esq.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					else:
						esq.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					i+=1
			if pag_atual +1 < len(qtd):
				i = qtd[pag_atual]
				while i <qtd[pag_atual+1]:
					if (i == 0):
						dir.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					elif (((self.profile.Get_V()[i-1])[2]) >= 50):
						dir.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					else:
						dir.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					i+=1
			sair = mudar = False
			score_aux = score_number
			#LACO DO MENU 2
			while (sair == False):
				score_number = score_aux
				#PEGA EVENTOS
				for evento in pygame.event.get():
					#EVENTOS DO MOUSE
					px , py = pygame.mouse.get_pos()
					if ((px>= 729)and (px<=760)) and ((py>= 82)and (py<=110)):
						ajuda = True
					else:
						ajuda = False
					if evento.type == pygame.MOUSEBUTTONUP:
						if Bleft == True:
							px , py = pygame.mouse.get_pos()
							if ((px>= 280)and (px<=348)) and ((py>= 500)and (py<=568)):
								msc_atual = 0
								if lado == 0:
									pag_atual -=2
									if pag_atual == -2:
										pag_atual = len(qtd)-2
										lado = 1
									sair = mudar = True
								else:
									lado = 0
									tam = len(dir)
							if ((px>= 450)and (px<=518)) and ((py>= 500)and (py<=568)):
								msc_atual = 0
								if lado == 1:
									pag_atual +=2
									if pag_atual >= (len(qtd)):
										pag_atual = 0
										lado = 0
									sair = mudar = True
								else:
									lado = 1
									tam = len(esq)
							if ((px>= 70)and (px<=270)) and ((py>= 510)and (py<=560)):
								btn_jogar.click()
								sair = True
							if ((px>= 530)and (px<=730)) and ((py>= 510)and (py<=560)):
								btn_voltar.click()
								mudar =voltar = sair = True
								#return False
							if (len(esq) > len(dir)):
								num = len(esq)
							else:
								num = len(dir)
							num2 = (-1)*(num/2)
							aux = Const_default_y+(num2*30)
							num2 =0
							for i in range(len(esq)):						
								if ((px>= 65)and (px<=397)) and ((py>= aux+30*num2) and (py<=aux+30*(num2)+25)):
									if (lado == 0)  and (msc_atual == num2):
										sair = True
									else:
										msc_atual = num2
										lado = 0
								num2 += 1
							num2 = 0
							for i in range(len(dir)):
								if ((px>= 415)and (px<=747)) and ((py>= aux+30*num2) and (py<=aux+30*(num2)+25)):
									if (lado == 1)  and (msc_atual == num2):
										sair = True
									else:
										msc_atual = num2
										lado = 1
								num2 += 1
							Bleft == False
					if evento.type == pygame.MOUSEBUTTONDOWN:
						Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
					if evento.type == pygame.QUIT:
						sys.exit(0)
					#EVENTOS DO TECLADO
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_RETURN:
							sair = True
						if evento.key == pygame.K_ESCAPE:
							return False
							msc_atual = -1
						if evento.key == pygame.K_LEFT:
							msc_atual = 0
							if lado == 0:
								pag_atual -=2
								if pag_atual == -2:
									pag_atual = len(qtd)-2
								lado = 1
								sair = mudar = True
							else:
								lado = 0
								tam = len(esq)
								
						if evento.key == pygame.K_RIGHT:
							msc_atual = 0
							if lado == 1:
								pag_atual +=2
								if pag_atual >= (len(qtd)):
									pag_atual = 0
								lado = 0
								sair = mudar = True
							else:
								lado = 1
								tam = len(dir)
						if evento.key == pygame.K_DOWN:
							msc_atual += 1
							if msc_atual > tam-1:
								msc_atual = 0
						if evento.key == pygame.K_UP:
							msc_atual -= 1
							if msc_atual < 0:
								msc_atual = tam-1
				
				#Desenha Fundo
				self.tela.blit(bkg,(0,0))
				#Escreve Numero das paginas esquerda e direita
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+1)), False, (226, 157, 54) ),(230,128))
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+2)), False, (226, 157, 54) ),(590,128))
				self.tela.blit(self.Carolingia_25.render(self.lang.Get(19), False, (226, 157, 54) ),(70,520))
				self.tela.blit(self.Carolingia_25.render(self.lang.Get(1), False, (226, 157, 54) ),(576,520))
				#self.tela.blit(self.Carolingia_25.render(("High Score:  "+repr(msc_atual)), False, (226, 157, 54) ),(0,0))
				#Desenha botoes
				self.tela.blit(btn_jogar.desenha(),(70,510))
				self.tela.blit(btn_red_e.desenha(),(280,500))
				self.tela.blit(btn_red_d.desenha(),(450,500))
				self.tela.blit(btn_voltar.desenha(),(530,510))
				#escreve texto dos botoes
				self.tela.blit(btn_list_text[0],(90,520))
				self.tela.blit(btn_list_text[2],(310,520))
				self.tela.blit(btn_list_text[3],(480,520))
				self.tela.blit(btn_list_text[1],(600,520))
				#ESCREVE ITENS DA PAGINA ESQUERDA
				if (len(esq) > len(dir)):
					num = len(esq)
				else:
					num = len(dir)
				num2 = (-1)*(num/2)
				for i in range(len(esq)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 0):
						if (i == msc_atual):
							self.tela.blit(selected,(60,aux-2))
						else:
							self.tela.blit(unselected,(60,aux-2))
					else:
						self.tela.blit(unselected,(60,aux-2))
					self.tela.blit(esq[i],(65,aux))
					self.tela.blit(self.Carolingia_20.render((repr((self.profile.Get_V()[score_number])[1])), False, (226, 157, 54) ),(330,aux))
					score_number+=1
				#ESCREVE ITENS DA PAGINA DIREITA
				num2 = (-1)*(num/2)
				for i in range(len(dir)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 1):
						if (i == msc_atual):
							self.tela.blit(selected,(410,aux-2))
						else:
							self.tela.blit(unselected,(410,aux-2))
					else:
						self.tela.blit(unselected,(410,aux-2))
					self.tela.blit(dir[i],(415,aux))
					self.tela.blit(self.Carolingia_20.render((repr((self.profile.Get_V()[score_number])[1])), False, (226, 157, 54) ),(700,aux))
					score_number+=1
				#DESENHA O MOUSE
				self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
				if ajuda == True:
					self.help()
				#atualiza a tela
				pygame.display.flip()
				if btn_jogar.getState() or btn_voltar.getState():
					time.sleep(0.2)
			#CHAMA GAMEPLAY
			if (msc_atual >= 0) and (mudar == False):
				if (pag_atual == 0) and lado == 0:
					music_number = msc_atual
				else:
					music_number =msc_atual+qtd[pag_atual-1+lado] 
				#print (repr(music_number))
				if (((self.profile.Get_V()[music_number-1])[2]) >= 50) or (music_number == 0):
					music = Music(Msc.GetOne(music_number))
					Game = Gameplay(self.tela, self.lang, music.GetTable(), music.GetName(), music.GetTempo(), self.config.Get_lvl(), self.config.Get_audio(), music.GetHeaderTicks())
					#recebe os valores de pontuacao
					point, miss, maxcombo,perform = Game.Play()
					if point == miss and miss == maxcombo and maxcombo==perform and perform == 0:
						#chama tela de exibicao
						self.Mostra(point,miss,maxcombo,perform)
					else:
						#verificar a pontuacao
						self.profile.Update_V(Msc.GetOne(music_number),point,perform)
						self.High_S.Update (Msc.GetOne(music_number),point, self.profile.nome)
						#salva a pontuacao
						self.profile.save()
						#chama tela de exibicao
						self.Mostra(point,miss,maxcombo,perform)
	#MENU DE QUICK PLAY
	def Menu_Q(self):
		Msc = Musics()
		btn_jogar = Button(0)
		btn_voltar = Button(0)
		btn_red_e = Button(1)
		btn_red_d = Button(1)
		btn_list_text = []
		btn_list_text.append(self.Old_English_25.render(self.lang.Get(19), False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render(self.lang.Get(1), False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render("<", False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render(">", False, (226, 157, 54) ))
		bkg = pygame.image.load("Graphics/Screens/Quick_play.jpg")
		selected = pygame.image.load("Graphics/Boxes/Selected.jpg")
		unselected = pygame.image.load("Graphics/Boxes/Unselected.jpg")
		qtd = 0
		qtd_opus = 0
		pag_atual = 0
		lado = 0
		msc_atual = 0
		aux = 0
		limit = 0
		
		list,qtd = Msc.GetList()
		esq = []
		dir = []
		tam = qtd[pag_atual]
		qtd_opus = len(qtd)
		voltar = False
		score_aux =score_number = 0
		ajuda = False
		#LACO DO MENU 1
		while (voltar == False):
			esq = []
			dir = []
			#CALCULA QUAIS PAGINAS MOSTRAR
			if pag_atual < qtd_opus:
				if pag_atual == 0:
					score_number= i = 0
					limit =qtd[pag_atual]
				else:
					score_number =i = qtd[pag_atual-1]
				while i < qtd[pag_atual]:
					esq.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					i+=1
			if pag_atual +1 < qtd_opus:
				i = qtd[pag_atual]
				while i <qtd[pag_atual+1]:
					dir.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					i+=1
			sair = mudar = False
			score_aux = score_number
			#LACO DO MENU 2
			while (sair == False):
				score_number = score_aux
				#PEGA EVENTOS
				for evento in pygame.event.get():
					#EVENTOS DO MOUSE
					px , py = pygame.mouse.get_pos()
					if ((px>= 729)and (px<=760)) and ((py>= 82)and (py<=110)):
						ajuda = True
					else:
						ajuda = False
					if evento.type == pygame.MOUSEBUTTONUP:
						if Bleft == True:
							px , py = pygame.mouse.get_pos()
							if ((px>= 280)and (px<=348)) and ((py>= 500)and (py<=568)):
								msc_atual = 0
								if lado == 0:
									pag_atual -=2
									if pag_atual <0:
										pag_atual = qtd_opus-2
										lado = 1
									sair = mudar = True
								else:
									lado = 0
									tam = len(dir)
							if ((px>= 450)and (px<=518)) and ((py>= 500)and (py<=568)):
								msc_atual = 0
								if lado == 1:
									pag_atual +=2
									if pag_atual > (qtd_opus-2):
										pag_atual = 0
										lado = 0
									sair = mudar = True
								else:
									lado = 1
									tam = len(esq)
							if ((px>= 70)and (px<=270)) and ((py>= 510)and (py<=560)):
								btn_jogar.click()
								sair = True
							if ((px>= 530)and (px<=730)) and ((py>= 510)and (py<=560)):
								btn_voltar.click()
								mudar =voltar = sair = True
								#return False
							if (len(esq) > len(dir)):
								num = len(esq)
							else:
								num = len(dir)
							aux = Const_default_y+(((-1)*(num/2))*30)
							num2 =0
							for i in range(len(esq)):						
								if ((px>= 65)and (px<=397)) and ((py>= aux+30*num2) and (py<=aux+30*(num2)+25)):
									if (lado == 0)  and (msc_atual == num2):
										sair = True
									else:
										msc_atual = num2
										lado = 0
								num2 += 1
							num2 = 0
							for i in range(len(dir)):
								if ((px>= 415)and (px<=747)) and ((py>= aux+30*num2) and (py<=aux+30*(num2)+25)):
									if (lado == 1)  and (msc_atual == num2):
										sair = True
									else:
										msc_atual = num2
										lado = 1
								num2 += 1
							Bleft == False
					if evento.type == pygame.MOUSEBUTTONDOWN:
						Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
					if evento.type == pygame.QUIT:
						sys.exit(0)
					#EVENTOS DO TECLADO
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_RETURN:
							sair = True
						if evento.key == pygame.K_ESCAPE:
							return False
							msc_atual = -1
						if evento.key == pygame.K_LEFT:
							msc_atual = 0
							if lado == 0:
								pag_atual -=2
								if pag_atual < 0:
									pag_atual = qtd_opus-2
								lado = 1
								sair = mudar = True
							else:
								lado = 0
								tam = len(esq)
								
						if evento.key == pygame.K_RIGHT:
							msc_atual = 0
							if lado == 1:
								pag_atual +=2
								if pag_atual >(qtd_opus-2):
									pag_atual = 0
								lado = 0
								sair = mudar = True
							else:
								lado = 1
								tam = len(dir)
						if evento.key == pygame.K_DOWN:
							msc_atual += 1
							if msc_atual > tam-1:
								msc_atual = 0
						if evento.key == pygame.K_UP:
							msc_atual -= 1
							if msc_atual < 0:
								msc_atual = tam-1
				
				#Desenha Fundo
				self.tela.blit(bkg,(0,0))
				#Escreve Numero das paginas esquerda e direita
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+1)), False, (226, 157, 54) ),(230,128))
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+2)), False, (226, 157, 54) ),(590,128))
				self.tela.blit(self.Carolingia_25.render(self.lang.Get(19), False, (226, 157, 54) ),(70,520))
				self.tela.blit(self.Carolingia_25.render(self.lang.Get(1), False, (226, 157, 54) ),(576,520))
				#self.tela.blit(self.Carolingia_25.render(("High Score:  "+repr(msc_atual)), False, (226, 157, 54) ),(0,0))
				#Desenha botoes
				self.tela.blit(btn_jogar.desenha(),(70,510))
				self.tela.blit(btn_red_e.desenha(),(280,500))
				self.tela.blit(btn_red_d.desenha(),(450,500))
				self.tela.blit(btn_voltar.desenha(),(530,510))
				#escreve texto dos botoes
				self.tela.blit(btn_list_text[0],(90,520))
				self.tela.blit(btn_list_text[2],(310,520))
				self.tela.blit(btn_list_text[3],(480,520))
				self.tela.blit(btn_list_text[1],(600,520))
				#ESCREVE ITENS DA PAGINA ESQUERDA
				if (len(esq) > len(dir)):
					num = len(esq)
				else:
					num = len(dir)
				num2 = (-1)*(num/2)
				for i in range(len(esq)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 0):
						if (i == msc_atual):
							self.tela.blit(selected,(60,aux-2))
						else:
							self.tela.blit(unselected,(60,aux-2))
					else:
						self.tela.blit(unselected,(60,aux-2))
					self.tela.blit(esq[i],(65,aux))
					self.tela.blit(self.Carolingia_20.render((repr((self.profile.Get_Q()[score_number])[1])), False, (226, 157, 54) ),(330,aux))
					score_number+=1
				#ESCREVE ITENS DA PAGINA DIREITA
				num2 = (-1)*(num/2)
				for i in range(len(dir)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 1):
						if (i == msc_atual):
							self.tela.blit(selected,(410,aux-2))
						else:
							self.tela.blit(unselected,(410,aux-2))
					else:
						self.tela.blit(unselected,(410,aux-2))
					self.tela.blit(dir[i],(415,aux))
					self.tela.blit(self.Carolingia_20.render((repr((self.profile.Get_Q()[score_number])[1])), False, (226, 157, 54) ),(700,aux))
					score_number+=1
				#DESENHA O MOUSE
				self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
				if ajuda == True:
					self.help()
				#atualiza a tela
				pygame.display.flip()
				if btn_jogar.getState() or btn_voltar.getState():
					time.sleep(0.2)
			#CHAMA GAMEPLAY
			if (msc_atual >= 0) and (mudar == False):
				if (pag_atual == 0) and lado == 0:
					music_number = msc_atual
				else:
					music_number =msc_atual+qtd[pag_atual-1+lado] #msc_atual+qtd[pag_atual]+lado
				#print (repr(msc_atual)+"|"+repr(qtd[pag_atual+lado])+"|"+repr(lado))
				# [0]1 [2]3 [4]5 [6]
				#print (music_number)
				#if (((self.profile.Get_V()[music_number-1])[2]) >= 50) or (music_number == 0):
				music = Music(Msc.GetOne(music_number))
				Game = Gameplay(self.tela, self.lang, music.GetTable(), music.GetName(), music.GetTempo(), self.config.Get_lvl(), self.config.Get_audio(), music.GetHeaderTicks())
				#recebe os valores de pontuacao
				point, miss, maxcombo,perform = Game.Play()
				if point == miss and miss == maxcombo and maxcombo==perform and perform == 0:
					#chama tela de exibicao
					self.Mostra(point,miss,maxcombo,perform)
				else:
					#verificar a pontuacao
					self.profile.Update_Q(Msc.GetOne(music_number),point)
					self.High_S.Update (Msc.GetOne(music_number),point, self.profile.nome)
					#salva a pontuacao
					self.profile.save()
					#chama tela de exibicao
					self.Mostra(point,miss,maxcombo,perform)
	#TELA DE HIGH SCORE
	def Menu_H(self):
		Msc = Musics()
		btn_general = Button(0)
		btn_voltar = Button(0)
		btn_red_e = Button(1)
		btn_red_d = Button(1)
		btn_list_text = []
		btn_list_text.append(self.Old_English_25.render(self.lang.Get(1), False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render("<", False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render(">", False, (226, 157, 54) ))
		bkg = pygame.image.load("Graphics/Screens/High_score.jpg")
		selected = pygame.image.load("Graphics/Boxes/Selected.jpg")
		unselected = pygame.image.load("Graphics/Boxes/Unselected.jpg")
		qtd = 0
		qtd_opus = 0
		pag_atual = 0
		lado = 0
		msc_atual = 0
		aux = 0
		limit = 0
		
		list,qtd = Msc.GetList()
		esq = []
		dir = []
		tam = qtd[pag_atual]
		qtd_opus = len(qtd)
		voltar = False
		score_aux =score_number = 0
		#LACO DO MENU 1
		while (voltar == False):
			esq = []
			dir = []
			#CALCULA QUAIS PAGINAS MOSTRAR
			if pag_atual < qtd_opus:
				if pag_atual == 0:
					score_number= i = 0
					limit =qtd[pag_atual]
				else:
					score_number =i = qtd[pag_atual-1]
				while i < qtd[pag_atual]:
					esq.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					i+=1
			if pag_atual +1 < qtd_opus:
				i = qtd[pag_atual]
				while i <qtd[pag_atual+1]:
					dir.append(self.Carolingia_20.render(arruma_texto(list[i]), False, (226, 157, 54) ))
					i+=1
			sair = mudar = False
			score_aux = score_number
			#LACO DO MENU 2
			while (sair == False):
				score_number = score_aux
				#PEGA EVENTOS
				for evento in pygame.event.get():
					#EVENTOS DO MOUSE
					if evento.type == pygame.MOUSEBUTTONUP:
						if Bleft == True:
							px , py = pygame.mouse.get_pos()
							if ((px>= 280)and (px<=348)) and ((py>= 500)and (py<=568)):
								msc_atual = 0
								if lado == 0:
									pag_atual -=2
									if pag_atual <0:
										pag_atual = qtd_opus-2
										lado = 1
									sair = mudar = True
								else:
									lado = 0
									tam = len(dir)
							if ((px>= 450)and (px<=518)) and ((py>= 500)and (py<=568)):
								msc_atual = 0
								if lado == 1:
									pag_atual +=2
									if pag_atual > qtd_opus-2:
										pag_atual = 0
										lado = 0
									sair = mudar = True
								else:
									lado = 1
									tam = len(esq)
							if ((px>= 530)and (px<=730)) and ((py>= 510)and (py<=560)):
								btn_voltar.click()
								mudar =voltar = sair = True
								#return False
							if (len(esq) > len(dir)):
								num = len(esq)
							else:
								num = len(dir)
							aux = Const_default_y+(((-1)*(num/2))*30)
							num2 =0
							for i in range(len(esq)):						
								if ((px>= 65)and (px<=397)) and ((py>= aux+30*num2) and (py<=aux+30*(num2)+25)):
									if (lado == 0)  and (msc_atual == num2):
										sair = True
									else:
										msc_atual = num2
										lado = 0
								num2 += 1
							num2 = 0
							for i in range(len(dir)):
								if ((px>= 415)and (px<=747)) and ((py>= aux+30*num2) and (py<=aux+30*(num2)+25)):
									if (lado == 1)  and (msc_atual == num2):
										sair = True
									else:
										msc_atual = num2
										lado = 1
								num2 += 1
							Bleft == False
					if evento.type == pygame.MOUSEBUTTONDOWN:
						Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
					if evento.type == pygame.QUIT:
						sys.exit(0)
					#EVENTOS DO TECLADO
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_RETURN:
							sair = True
						if evento.key == pygame.K_ESCAPE:
							return False
							msc_atual = -1
						if evento.key == pygame.K_LEFT:
							msc_atual = 0
							if lado == 0:
								pag_atual -=2
								if pag_atual <0:
									pag_atual = qtd_opus-2
								lado = 1
								sair = mudar = True
							else:
								lado = 0
								tam = len(esq)
								
						if evento.key == pygame.K_RIGHT:
							msc_atual = 0
							if lado == 1:
								pag_atual +=2
								if pag_atual > qtd_opus-2:
									pag_atual = 0
								lado = 0
								sair = mudar = True
							else:
								lado = 1
								tam = len(dir)
						if evento.key == pygame.K_DOWN:
							msc_atual += 1
							if msc_atual > tam-1:
								msc_atual = 0
						if evento.key == pygame.K_UP:
							msc_atual -= 1
							if msc_atual < 0:
								msc_atual = tam-1
				
				#Desenha Fundo
				self.tela.blit(bkg,(0,0))
				#Escreve Numero das paginas esquerda e direita
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+1)), False, (226, 157, 54) ),(230,128))
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+2)), False, (226, 157, 54) ),(590,128))
				self.tela.blit(self.Carolingia_25.render(self.lang.Get(1), False, (226, 157, 54) ),(576,520))
				#self.tela.blit(self.Carolingia_25.render(("High Score:  "+repr(msc_atual)), False, (226, 157, 54) ),(0,0))
				#Desenha botoes
				self.tela.blit(btn_general.desenha(),(70,510))
				self.tela.blit(btn_red_e.desenha(),(280,500))
				self.tela.blit(btn_red_d.desenha(),(450,500))
				self.tela.blit(btn_voltar.desenha(),(530,510))
				#escreve texto dos botoes
				#self.tela.blit(btn_list_text[0],(90,520))
				self.tela.blit(btn_list_text[1],(310,520))
				self.tela.blit(btn_list_text[2],(480,520))
				self.tela.blit(btn_list_text[0],(600,520))
				#ESCREVE ITENS DA PAGINA ESQUERDA
				if (len(esq) > len(dir)):
					num = len(esq)
				else:
					num = len(dir)
				num2 = (-1)*(num/2)
				for i in range(len(esq)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 0):
						if (i == msc_atual):
							self.tela.blit(selected,(60,aux-2))
						else:
							self.tela.blit(unselected,(60,aux-2))
					else:
						self.tela.blit(unselected,(60,aux-2))
					self.tela.blit(esq[i],(65,aux))
					self.tela.blit(self.Carolingia_20.render((repr((self.High_S.Get()[score_number])[1])), False, (226, 157, 54) ),(330,aux-2))
					score_number+=1
				#ESCREVE ITENS DA PAGINA DIREITA
				num2 = (-1)*(num/2)
				for i in range(len(dir)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 1):
						if (i == msc_atual):
							self.tela.blit(selected,(410,aux-2))
						else:
							self.tela.blit(unselected,(410,aux-2))
					else:
						self.tela.blit(unselected,(410,aux-2))
					self.tela.blit(dir[i],(415,aux))
					self.tela.blit(self.Carolingia_20.render((repr((self.High_S.Get()[score_number])[1])), False, (226, 157, 54) ),(700,aux))
					score_number+=1
				#DESENHA O MOUSE
				self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
				#ATUALIZA A TELA
				pygame.display.flip()
				if btn_voltar.getState():
					time.sleep(0.2)
			esq = []
			dir = []
	#TELA DE ACHIEVMENTS
	def Menu_A(self):
		Arch = self.profile.Return_Achie()
		#carrega imagens
		btn_general = Button(0)
		btn_voltar = Button(0)
		btn_red_e = Button(1)
		btn_red_d = Button(1)
		btn_list_text = []
		btn_list_text.append(self.Old_English_25.render(self.lang.Get(1), False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render("<", False, (226, 157, 54) ))
		btn_list_text.append(self.Old_English_25.render(">", False, (226, 157, 54) ))
		bkg = pygame.image.load("Graphics/Screens/Achievment.jpg")
		selected = pygame.image.load("Graphics/Boxes/Selected.jpg")
		unselected = pygame.image.load("Graphics/Boxes/Unselected.jpg")
		#inicia variaveis
		qtd = 0
		pag_atual = 0
		lado = 0
		msc_atual = 0
		aux = 0
		limit = 0

		list,qtd = Arch.return_table()
		esq = []
		dir = []
		tam = qtd[pag_atual]
		voltar = False
		score_aux =score_number = 0
		
		#LACO DO MENU 1
		while (voltar == False):
			esq = []
			dir = []
			#CALCULA QUAIS PAGINAS MOSTRAR
			if ( pag_atual > len(qtd)):
				 pag_atual = 0
			if pag_atual < len(qtd):
				if pag_atual == 0:
					score_number= i = 0
					limit =qtd[pag_atual]
				else:
					score_number =i = qtd[pag_atual-1]
				while i < qtd[pag_atual]:
					esq.append(self.Carolingia_20.render(self.lang.Get(28+i), False, (255*(1-list[i][1]),0,0) ))
					i+=1
			if pag_atual +1 < len(qtd):
				i = qtd[pag_atual]
				while i <qtd[pag_atual+1]:
					dir.append(self.Carolingia_20.render(self.lang.Get(28+i), False, (255*(1-list[i][1]),0,0) ))
					i+=1
			
			sair = mudar = False
			score_aux = score_number
			#LACO DO MENU 2
			while (sair == False):
				score_number = score_aux
				#PEGA EVENTOS
				for evento in pygame.event.get():
					#EVENTOS DO MOUSE
					if evento.type == pygame.MOUSEBUTTONUP:
						if Bleft == True:
							px , py = pygame.mouse.get_pos()
							if ((px>= 80)and (px<=105)) and ((py>= 462)and (py<=487)):
								msc_atual = 0
								if lado == 0:
									pag_atual -=2
									if pag_atual < -2:
										pag_atual = 4
										lado = 1
									sair = mudar = True
								else:
									lado = 0
									tam = len(dir)
							if ((px>= 695)and (px<=720)) and ((py>= 462)and (py<=487)):
								msc_atual = 0
								if lado == 1:
									pag_atual +=2
									if pag_atual == 6:
										pag_atual = 0
										lado = 0
									sair = mudar = True
								else:
									lado = 1
									tam = len(esq)
							#if ((px>= 50)and (px<=250)) and ((py>= 510)and (py<=560)):
							#	sair = True
							if ((px>= 530)and (px<=730)) and ((py>= 510)and (py<=560)):
								btn_voltar.click()
								voltar = sair = True


							aux = Const_default_y
							for i in range(len(esq)):
								if ((px>= 65)and (px<=397)) and ((py>= aux)and (py<=aux+25)):
									if (lado == 0)  and (msc_atual == ((aux - Const_default_y)/30)):
										sair = True
									else:
										msc_atual = int ((aux - Const_default_y)/30)
										lado = 0
								aux+=30

							aux = Const_default_y
							for i in range(len(dir)):
								if ((px>= 415)and (px<=747)) and ((py>= aux)and (py<=aux+25)):
									if (lado == 1)  and (msc_atual == ((aux - Const_default_y)/30)):
										sair = True
									else:
										msc_atual = int ((aux - Const_default_y)/30)
										lado = 1
								aux+=30
							Bleft == False
					if evento.type == pygame.MOUSEBUTTONDOWN:
						Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
					if evento.type == pygame.QUIT:
						sys.exit(0)
					#EVENTOS DO TECLADO
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_RETURN:
							sair = True
						if evento.key == pygame.K_ESCAPE:
							return False
							msc_atual = -1
						if evento.key == pygame.K_LEFT:
							msc_atual = 0
							if lado == 0:
								pag_atual -=2
								if pag_atual == -2:
									pag_atual = 2
									lado = 0
								sair = mudar = True
							else:
								lado = 0
								tam = len(esq)
						if evento.key == pygame.K_RIGHT:
							msc_atual = 0
							if lado == 1:
								pag_atual +=2
								if pag_atual == 4:
									pag_atual = 0
									lado = 0
								sair = mudar = True
							else:
								lado = 1
								tam = len(dir)
								if pag_atual == 4:
									pag_atual = 0
									lado = 0
						if evento.key == pygame.K_DOWN:
							msc_atual += 1
							if msc_atual > tam-1:
								msc_atual = 0
						if evento.key == pygame.K_UP:
							msc_atual -= 1
							if msc_atual < 0:
								msc_atual = tam-1

				#Desenha Fundo
				self.tela.blit(bkg,(0,0))
				#Escreve Numero das paginas esquerda e direita
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+1)), False, (226, 157, 54) ),(230,128))
				self.tela.blit(self.Carolingia_20.render((repr(pag_atual+2)), False, (226, 157, 54) ),(590,128))
				#self.tela.blit(self.Carolingia_25.render(self.lang.Get(19), False, (226, 157, 54) ),(70,520))
				self.tela.blit(self.Carolingia_25.render(self.lang.Get(1), False, (226, 157, 54) ),(576,520))
				#self.tela.blit(self.Carolingia_25.render(("Achivments \o/:  "), False, (226, 157, 54) ),(0,0))
				#Desenha botoes
				self.tela.blit(btn_general.desenha(),(70,510))
				self.tela.blit(btn_red_e.desenha(),(280,500))
				self.tela.blit(btn_red_d.desenha(),(450,500))
				self.tela.blit(btn_voltar.desenha(),(530,510))
				#escreve texto dos botoes
				#self.tela.blit(btn_list_text[0],(90,520))
				self.tela.blit(btn_list_text[1],(310,520))
				self.tela.blit(btn_list_text[2],(480,520))
				self.tela.blit(btn_list_text[0],(600,520))
				#ESCREVE ITENS DA PAGINA ESQUERDA
				if (len(esq) > len(dir)):
					num = len(esq)
				else:
					num = len(dir)
				num2 = (-1)*(num/2)
				for i in range(len(esq)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 0):
						if (i == msc_atual):
							self.tela.blit(selected,(60,aux-2))
						else:
							self.tela.blit(unselected,(60,aux-2))
					else:
						self.tela.blit(unselected,(60,aux-2))
					self.tela.blit(esq[i],(65,aux))
					#self.tela.blit(self.Carolingia_20.render((repr((self.profile.Get_V()[score_number])[1])), False, (226, 157, 54) ),(330,aux))
					score_number+=1
				#ESCREVE ITENS DA PAGINA DIREITA
				num2 = (-1)*(num/2)
				for i in range(len(dir)):
					aux = Const_default_y+(num2*30)
					num2 += 1
					if (lado == 1):
						if (i == msc_atual):
							self.tela.blit(selected,(410,aux-2))
						else:
							self.tela.blit(unselected,(410,aux-2))
					else:
						self.tela.blit(unselected,(410,aux-2))
					self.tela.blit(dir[i],(415,aux))
					#self.tela.blit(self.Carolingia_20.render((repr((self.profile.Get_V()[score_number])[1])), False, (226, 157, 54) ),(700,aux))
					score_number+=1
				#DESENHA O MOUSE
				self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
				#atualiza a tela
				pygame.display.flip()
				if btn_voltar.getState():
					time.sleep(0.2)
	#TELA DE OPCOES
	def Option(self):
		btn_salvar = Button(0)
		btn_cancelar = Button(0)
		sair = False
		#variaveis de config
		Nivel = [self.lang.Get(10),self.lang.Get(11),self.lang.Get(12),self.lang.Get(13)]
		nivel =[1,2,5,10]
		language = self.languages.GetNameList()
		lang_id = 0
		lvl = 0
		full = self.config.Get_full()
		audio = self.config.Get_audio()
		for i in nivel:
			if (i == self.config.Get_lvl()):
				break
			lvl +=1
		y=0;
		bkg = pygame.image.load("Graphics/Screens/Option.jpg")
		bar = pygame.image.load("Graphics/Boxes/Bar.jpg")
		#LACO DO MENU
		while (sair == False):
			#PREPARA PARA Desenha
			if full == 1:
				checkbox= pygame.image.load("Graphics/Boxes/Checked.jpg")
			else:
				checkbox= pygame.image.load("Graphics/Boxes/Unchecked.jpg")
			#PEGA EVENTOS
			for evento in pygame.event.get():
				#EVENTOS DO MOUSE
				if evento.type == pygame.MOUSEBUTTONUP:
					if Bleft == True:
						px , py = pygame.mouse.get_pos()
						#botao de salvar
						if ((px>= 50)and (px<=250)) and ((py>= 510)and (py<=560)):
							btn_salvar.click()
							self.config.Set(nivel[lvl], audio, full,language[lang_id])
							self.profile.Set_Conf(self.config)
							self.config = self.profile.Return_Config()
							#carregando linguagem
							self.languages = Language(self.config.Get_lang())
							self.lang = Lang (self.languages.GetOne())
							self.profile.save()
							sair = True
						#botao de cancelar
						if ((px>= 550)and (px<=750)) and ((py>= 510)and (py<=560)):
							btn_cancelar.click()
							sair = True
						Bleft == False
				if evento.type == pygame.MOUSEBUTTONDOWN:
					Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
				#EVENTOS DO TECLADO
				if evento.type == pygame.QUIT:
					sys.exit()
				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_RETURN:
						#salva as configuracoes
						self.config.Set(nivel[lvl], audio, full,language[lang_id])
						self.profile.Set_Conf(self.config)
						self.config = self.profile.Return_Config()
						#carregando linguagem
						self.languages = Language(self.config.Get_lang())
						self.lang = Lang (self.languages.GetOne())
						#print (self.languages.GetOne())
						self.profile.save()
						sair = True
					if evento.key == pygame.K_ESCAPE:
						sair = True
					if evento.key == pygame.K_LEFT:
						if (y == 0):
							lvl -=1
							if lvl <0:
								lvl = 3
						elif (y== 1):
							if audio >0.0:
								audio -=0.1
							if audio <0.0:
								audio = 0.0
						elif (y==2):
							if (full == 1):
								full = 0
							else:
								full = 1
						else:
							lang_id -=1
							if lang_id <0:
								lang_id = len(language)-1
					if evento.key == pygame.K_RIGHT:
						if (y == 0):
							lvl +=1
							if lvl >3:
								lvl = 0
						elif (y== 1):
							if audio <1.0:
								audio +=0.1
							if audio >1.0:
								audio = 1.0
						elif (y==2):
							if (full == 1):
								full = 0
							else:
								full = 1
						else:
							lang_id +=1
							if lang_id >len(language)-1:
								lang_id = 0
					if evento.key == pygame.K_DOWN:
						y += 1
						if y > 3:
							y = 0
					if evento.key == pygame.K_UP:
						y -= 1
						if y < 0:
							y = 3
			#DESENHA FUNDO
			self.tela.blit(bkg,(0,0))
			#self.tela.blit(self.Carolingia_25.render(("Options:  "+repr(y)), False, (226, 157, 54) ),(0,0))
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(16), False, (226, 157, 54) ),(90,610))
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(17), False, (226, 157, 54) ),(596,610))
			#opcoes
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(22), False, (226, 157, 54) ),(120,236))
			self.tela.blit(self.Carolingia_25.render((Nivel[lvl]), False, (226, 157, 54) ),(315,236))
			
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(23), False, (226, 157, 54) ),(120,306))
			self.tela.blit(pygame.transform.scale(bar ,(int (180*audio), 36)),(308,306))
			
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(24), False, (226, 157, 54) ),(120,376))
			self.tela.blit(checkbox,(308,376))
			
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(25), False, (226, 157, 54) ),(120,446))
			self.tela.blit(self.Carolingia_25.render((language[lang_id]), False, (226, 157, 54) ),(315,446))
			#Desenha botoes
			self.tela.blit(btn_salvar.desenha(),(50,510))
			self.tela.blit(btn_cancelar.desenha(),(550,510))
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(16), False, (226, 157, 54) ),(70,520))
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(17), False, (226, 157, 54) ),(576,520))
			#desenha seta de selecionado
			self.tela.blit(pygame.transform.rotate(self.cursor_picture,-125), (55,227+70*y))
			#DESENHA O MOUSE
			self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
			#ATUALIZA A TELA
			pygame.display.flip()
			if btn_salvar.getState() or btn_cancelar.getState():
					time.sleep(0.2)
	#TELA POS JOGO
	def Mostra(self,score,miss,maxcombo,perform):
		# chama teste de achieviment aqui
		self.profile.set_achiev( testa_achie(self.config.Get_lvl(),miss,maxcombo,perform) )
		if perform >=98:
			letra = "S"
		elif perform >89 and perform <= 97:
			letra = "A"
		elif perform >69 and perform <=89:
			letra = "B"
		elif perform >49 and perform <=69:
			letra = "C"
		elif perform >39 and perform <=49:
			letra = "D"
		elif perform >19 and perform <=39:
			letra = "E"
		else:
			letra = "Z"
		bkg = pygame.image.load("Graphics/Screens/Achievment.jpg")
		s_letra = pygame.image.load("Graphics/Chars/"+letra+".jpg")
		sair = False
		y=0;
		
		while (sair == False):
			#PEGA EVENTOS
			for evento in pygame.event.get():
				#EVENTOS DO MOUSE
				if evento.type == pygame.MOUSEBUTTONUP:
					if Bleft == True:
						px , py = pygame.mouse.get_pos()
						if ((px>= 550)and (px<=750)) and ((py>= 510)and (py<=560)):
							return False
						Bleft == False
				if evento.type == pygame.MOUSEBUTTONDOWN:
					Bleft,Bmiddle, Bright =  pygame.mouse.get_pressed()
				if evento.type == pygame.QUIT:
					sair = True
				#EVENTOS DO TECLADO
				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_RETURN:
							sair = True
					if evento.key == pygame.K_ESCAPE:
						sair = True
			#DESENHA FUNDO
			self.tela.blit(bkg,(0,0))
			#ESCREVE DADOS DO JOGO
			self.tela.blit(self.Carolingia_25.render(self.lang.Get(1), False, (226, 157, 54) ),(576,520))
			self.tela.blit(self.Carolingia_25.render((self.lang.Get(14)+":  "), False, (226, 157, 54) ),(300,100))
			self.tela.blit(self.Carolingia_25.render((repr(score)), False, (226, 157, 54) ),(300,150))
			self.tela.blit(s_letra,(300,200))
			self.tela.blit(self.Carolingia_25.render(("MaxCombo:  "+repr(maxcombo)), False, (226, 157, 54) ),(300,400))
			self.tela.blit(self.Carolingia_25.render((self.lang.Get(15)+":  "+repr(miss)), False, (226, 157, 54) ),(300,450))
			#DESENHA O MOUSE
			self.tela.blit(self.cursor_picture, pygame.mouse.get_pos())
			#ATUALIZA A TELA
			pygame.display.flip()
	
	def help(self):
		pygame.draw.rect(self.tela, (255, 255, 255), (50,80,700,400), 0)
		self.tela.blit(self.Carolingia_25.render((self.lang.Get(26)), False, (226, 157, 54) ),(300,100))
		self.tela.blit(self.Carolingia_25.render((self.lang.Get(27)), False, (226, 157, 54) ),(50,150))