#coding: utf-8
import datetime
import sys
from Config import *
from Achievement import *
class Profile:
    nome = ""
    data_criacao = ""
    ultimo_jogo = ""
    recordes_gameplay = []
    recordes_quickplay =[]
    config = None
    MyArch = None
    def __init__ (self,arquivo="Default"):
        self.recordes_gameplay = []
        self.recordes_quickplay =[]
        musics= []
        self.MyArch = Achievement()
        temp = ''
        try:
            file = open ('Data/Musics.vts','r')
            tag = 0
            for i in file:
                #se encontra a tag
                if (i[0] == "["):
                    try:
                        aux = i.replace('[','')
                        aux = aux.replace(']','')
                        aux = ''.join(aux.split())
                        tag = int(aux)
                        if (tag > 0):
                            continue
                        else:
                            raise ValueError
                    except ValueError:
                        print ("erro: tag invalida em Profile.vts")
                #se a tag marca algum opus
                if tag != 0:
                    #adiciona a musica na lista
                    musics.append(''.join(i.split()))
            file.close()
        except IOError:
            sys.exit()
        try:
            #arquivo = arquivo.replace("\n", "")
            arquivo = ''.join(arquivo.split())
            file = open ('Data/Profiles/'+arquivo+'.vts','r')
            cont =0
            cont2 = 0
            separador = -1
            nivel,audio,full = 226, 157, 54
            lang =''
            for i in file:
                #achou separador entre 'be a virtuosi' e 'quick play' scores
                if i.startswith ('#'):
                    separador = separador+1
                    cont = 0
                elif separador == -1:
                    #pega os dados do profile
                    if (cont == 0):
                        self.nome = ''.join(i.split())
                    elif (cont == 1):
                        self.data_criacao =  ''.join(i.split())
                    elif (cont == 2):
                        self.ultimo_jogo =  ''.join(i.split())
                    elif (cont == 3):
                        nivel = int(''.join(i.split()))
                    elif (cont == 4):
                        audio = float (''.join(i.split()))
                    elif (cont == 5):
                        full = int(''.join(i.split()))
                    elif (cont == 6):
                        lang = ''.join(i.split())
                        separador = 0
                elif separador == 0:
                    nome, score, perf = i.split('#')
                    for j in musics:
                        #se a musica da lista esta no arquivo de profile carrega a pontuacao
                        if j == nome:
                            self.recordes_gameplay.append([nome,int(score),int(perf)])
                            flag = 1
                    # se nao achou a musica adiciona nota 0
                    """if flag == 0:
                        self.recordes_gameplay.append([j,0,0])"""
                elif separador == 1:
                    flag = 0
                    nome, score= i.split('#')
                    for j in musics:
                        #se a musica da lista esta no arquivo de profile carrega a pontuacao
                        if j == nome:
                            self.recordes_quickplay.append([nome,int(score)])
                            flag = 1
                    # se nao achou a musica adiciona nota 0
                    """if flag == 0:
                        self.recordes_quickplay.append([j,0])"""
                elif separador == 2:
                    temp +=i
                cont += 1
            file.close()
            self.MyArch.load(temp)
            self.config = Config(nivel,audio,full,lang)
        except IOError:
            self.nome = arquivo
            now = datetime.datetime.now()
            self.ultimo_jogo = now.strftime("%Y-%m-%d %H:%M")
            self.data_criacao = now.strftime("%Y-%m-%d %H:%M")
            self.config = Config(2,1.0,1,"Portugues Brasileiro")
            if len(self.recordes_gameplay) == 0:
                for j in musics:
                    self.recordes_gameplay.append([j,0,0])
            if len(self.recordes_quickplay) == 0:
                for j in musics:
                    self.recordes_quickplay.append([j,0])
            self.save()

    def Return_Config (self):
        return self.config
            
    def Return_Achie (self):
        return self.MyArch
    
    def Set_Conf(self, config):
        #print (config.Get_lang())
        self.config = Config(config.Get_lvl(),config.Get_audio(),config.Get_full(),config.Get_lang())
            
    def Get_V(self):
        return self.recordes_gameplay
    
    def Get_Q(self):
        return self.recordes_quickplay
    
    def Update_V(self,music_name, score,perf):
        for i in self.recordes_gameplay:
            if i[0] == music_name:
                if int(i[1]) < score:
                    i[1] = score
                    i[2] = perf
    
    def Update_Q(self,music_name, score):
        for i in self.recordes_quickplay:
            if i[0] == music_name:
                if int(i[1]) < score:
                    i[1] = score

    def save(self):
        #self.nome = self.nome.replace("\n", "")
        self.nome = ''.join(self.nome.split())
        file = open ('Data/Profiles/'+self.nome+'.vts','w')
        now = datetime.datetime.now()
        self.ultimo_jogo = now.strftime("%Y-%m-%d %H:%M")


        file.write(self.nome+"\n")
        self.data_criacao = ''.join(self.data_criacao.split())
        file.write(self.data_criacao+"\n")
        file.write(self.ultimo_jogo+"\n")

        file.write(repr(self.config.Get_lvl())+"\n")
        file.write(repr(self.config.Get_audio())+"\n")
        file.write(repr(self.config.Get_full())+"\n")
        file.write(''.join(self.config.Get_lang().split())+"\n")

        for i in self.recordes_gameplay:
            file.write (i[0]+"#"+repr(i[1])+"#"+repr(i[2])+"\n")
        file.write("#\n")
        for i in self.recordes_quickplay:
            file.write (i[0]+"#"+repr(i[1])+"\n")
        file.write("#\n")
        #salva achieviments
        file.write(self.MyArch.save())
        file.close()

    def set_achiev(self, id):
        self.MyArch.setAchie(id)
            
class Profiles:
    profiles = []
    def __init__ (self):
        self.profiles = []
    def GetOne(self):
        return ''.join(self.profiles[0].split())
        """if self.profiles[0][-1] == "\n":
            return self.profiles[0][:-1]
        else:
            return self.profiles[0]"""
            
    def GetList(self):
        return self.profiles
            
    def MoveUp(self,item):
        self.profiles.remove(item)
        self.profiles.insert(0,item)
        self.Save()
    def RmvOne(self, item):
        flag = 0
        for i in self.profiles:
            if item == i:
                self.profiles.remove(item)
        self.Save()
        self.Load()
    def AddOne(self, item):
        flag = 0
        for i in self.profiles:
            if item == i:
                flag = 1
        if flag == 0:
            self.profiles.insert(0,item)
    def Load(self):
        if self.profiles != []:
            del self.profiles
        self.profiles = []
        file = open ('Data/Profiles.vts','r')
        #file.readline()
        for i in file:
            self.profiles.append(''.join(i.split()))
        file.close()
    def Save(self):
        file = open ('Data/Profiles.vts','w')
        for i in self.profiles:
            file.write(''.join(i.split())+"\n")
        file.close()
