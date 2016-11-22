
#for /F %i in (Musics.vts) do c:\users\helder\desktop\versao1.5\MidCsv\Midicsv.exe < c:\users\helder\desktop\versao1.5\data\musics\%i.mid > c:\users\helder\desktop\versao1.5\%i.txt
#coding: utf-8
import sys
import Extras
from Generate import *
import time
from operator import itemgetter, attrgetter
import platform
import re
class Music:
    nome = ""
    notas = []
    file = ''
    header = 0
    list_temp = []
    #construtor
    def __init__ (self,filename="mozart-allegro_vivace"):
        try:
            self.nome = filename
            self.file =filename
            self.CreateTable()
        except IOError:
            #tratar caso arquivo nao existe
            i = 0
    #de string para decima
    def dec (self,s):
        aux = 0
        cont = 0
        while cont < len(s):
            aux = aux + pow(2, cont)*int(s[cont])
            cont += 1
        return aux
    #de int para string binaria
    def bin1(self,s):
        aux = ''
        if s<=1:
            return str(s)
        else:
            return (self.bin1(s>>1) + str(s&1))
    #retorna nome
    def GetName(self):
        return self.nome
    #retorna tabela
    def GetTable(self):
        return self.notas
    #retorna o tempo da musica
    def GetTempo(self):
        return self.list_temp
    #retorna o header de ticks da musica
    def GetHeaderTicks(self):
        return int(self.header)
    
    def cria_event(self, arq):
        progresso = 0
        table = []
        ok = 0
        arq = arq[0:-1]
        table = [linha for linha in re.split(r'\\r\\n|\n', arq) if linha.strip()]
        f = open ('table.txt','w')
        f.write(str(table))
        f.close()
        list_live = []
        tempo_count = 0
        for i in table:
            progresso +=1
            if progresso/len(table) % 3 == 1:
                Extras.Load(50+50*(progresso/len(table)))
                time.sleep(0.005)
            if ok == 0:
                line = i.split(', ')
                if len(line) > 2:
                    #encontrar o "tempo" certo
                    if ((line[2].find('Header') != -1) or (line[2].find('header') != -1)):
                        self.header = int(line[5])
                    if ((line[2].find('Instrument_name_t') != -1) or (line[2].find('Text_t') != -1) or (line[2].find('Title_t') != -1)):
                        if ((line[3].find('Violin') != -1) or (line[3].find('violin')!= -1)):
                            ok = 1
            else:
                line = i.split(', ')
                if line[2].find('Note_on_c') != -1:
                    if line[5] != 0:
                        list_live.append([int(line[1]),int(line[4]),0])
                        j = list_live[len(list_live)-2]
                        j[2] = int(line[1])
                    else:
                        j = list_live[len(list_live)-1]
                        j[2] = int(line[1])
                if line[2].find('Note_off_c') != -1:
                    j = list_live[len(list_live)-1]
                    j[2] = int(line[1])
                if line[2].find('End_track') != -1:
                    ok = 0
                    #break
        print ("comecando ordenacao")
        list_live =sorted(list_live, key=itemgetter(0)) 
        print ("ordenado")
        if len(list_live)>0:
            ok = 1
        for i in table:
            line = i.split(', ')
            if len(line) > 2:
                if line[2].find('Tempo') != -1:
                        self.list_temp.append([int(line[1]),int(line[3])])
        #        tempo_count += -1
        #        if tempo_count == 0:
        #            print(self.tempo)
                #return [[0,75]]
        if len(self.list_temp) ==0:
            self.list_temp.append([0,500000])
        if ok == 1:
            return list_live
        else:
            print ("sem violino")
            return None
    #cria tabela
    def CreateTable(self):
        Extras.Load(0)
        time.sleep(0.5)
        Extras.Load(10)
        time.sleep(0.5)
        Extras.Load(20)
        time.sleep(0.5)
        gen = Generate(self.file)
        Extras.Load(50)
        time.sleep(0.5)
        self.notas = self.cria_event(gen.generateit())
        Extras.Load(100)

class Musics:
    qtd = []
    musics = []
    def __init__ (self):
        self.musics = []
        self.Load()
    def GetOne(self,i):
        return self.musics[i]
        
    def GetList(self):
        return self.musics, self.qtd
        
    def Load(self):
        self.qtd = []
        self.musics = []
        file = open ('Data/Musics.vts','r')
        cont = 0
        tag = 0
        string_aux = ''
        for i in file:
            aux = 0
            #se encontra a tag
            if (i[0] == "["):
                if (len (self.qtd)==0):
                    self.qtd.append(0)
                else:
                    self.qtd.append(self.qtd[len(self.qtd)-1])
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
                    print ("erro: tag invalida em Musics.vts")
            #se a tag marca algum opus
            if tag != 0:
                string_aux = ''.join(i.split())
                #adiciona a musica na lista
                self.musics.append(string_aux)
                #incrementa a qtd de musicas do opus atual
                self.qtd[len(self.qtd)-1] +=1
        file.close()
    # somente se le o arquivo
    # criar music list maker se necessario!!
    #def Save(self):
    #    file = open ('Data/Music_list.vts','w')
    #    for i in self.musics:
    #        file.write(i+"<br>")
    #    file.close()
