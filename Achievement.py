#coding: utf-8
import sys
"""
    completar 1 musica facil com 95%
    completar 1 musica normal com 95%
    completar 1 musica dificil com 95%
    completar 1 musica virtuosa com 95%
    completar 5 musica facil com 95%
    completar 5 musica normal com 95%
    completar 5 musica dificil com 95%
    completar 5 musica virtuosa com 95%
    completar 1 musica facil com 100%
    completar 1 musica normal com 100%
    completar 1 musica dificil com 100%
    completar 1 musica virtuosa com 100%
"""
class Achievement:
    Arch = None
    def __init__ (self):
        i = 0
        self.Arch = []
        #[numero, nome, flag]
        #[numero, nome, flag, contador]
        self.Arch.append([0,0])
        self.Arch.append([1,0])
        self.Arch.append([2,0])
        self.Arch.append([3,0])
        self.Arch.append([4,0,0])
        self.Arch.append([5,0,0])
        self.Arch.append([6,0,0])
        self.Arch.append([7,0,0])
        self.Arch.append([8,0])
        self.Arch.append([9,0])
        self.Arch.append([10,0])
        self.Arch.append([11,0])
    def getAchie(self, id=0):
        return self.Arch[id][1]
    def setAchie(self, id=0):
        #print (id)
        if (id == 0):
            self.Arch[id][1] = 1 
        elif (id == 1):
            self.Arch[id][1] = 1 
        elif (id == 2):
            self.Arch[id][1] = 1 
        elif (id == 3):
            self.Arch[id][1] = 1 
        elif (id == 4):
            self.Arch[id][2] += 1
            if self.Arch[id][2] == 5:
                self.Arch[id][1] = 1
        elif (id == 5):
            self.Arch[id][2] += 1
            if self.Arch[id][2] == 5:
                self.Arch[id][1] = 1
        elif (id == 6):
            self.Arch[id][2] += 1
            if self.Arch[id][2] == 5:
                self.Arch[id][1] = 1
        elif (id == 7):
            self.Arch[id][2] += 1
            if self.Arch[id][2] == 5:
                self.Arch[id][1] = 1
        elif (id == 8):
            self.Arch[0][1] = 1 
            self.Arch[4][2] += 1
            self.Arch[id][1] = 1
            self.Arch[id-4][2] += 1
            if self.Arch[id-4][2] == 5:
                self.Arch[id-4][1] = 1
        elif (id == 9):
            self.Arch[1][1] = 1 
            self.Arch[5][2] += 1
            self.Arch[id][1] = 1 
            self.Arch[id-4][2] += 1
            if self.Arch[id-4][2] == 5:
                self.Arch[id-4][1] = 1
        elif (id == 10):
            self.Arch[2][1] = 1 
            self.Arch[6][2] += 1
            self.Arch[id][1] = 1 
            self.Arch[id-4][2] += 1
            if self.Arch[id-4][2] == 5:
                self.Arch[id-4][1] = 1
        elif (id == 11):
            self.Arch[3][1] = 1 
            self.Arch[7][2] += 1
            self.Arch[id][1] = 1 
            self.Arch[id-4][2] += 1
            if self.Arch[id-4][2] == 5:
                self.Arch[id-4][1] = 1
    
    def return_table(self):
        return self.Arch, [4,8,12]
            
    def load(self, arquivo):
        file = arquivo.split('\n')
        cont = 0
        for i in file:
            if i == '':
                break
            tupla = i.split("#")
            if len(tupla) == 2:
                self.Arch[cont][0] = int(tupla[0])
                self.Arch[cont][1] = int(tupla[1])
            else:
                self.Arch[cont][0] = int(tupla[0])
                self.Arch[cont][1] = int(tupla[1])
                self.Arch[cont][2] = int(tupla[2])
            cont += 1
        #print (self.Arch)
    def save(self):
        temp = ''
        for i in range(4):
            temp +=(repr(self.Arch[i][0]) +"#"+repr(self.Arch[i][1])+"\n")
        for i in range(4,8):
            temp += (repr(self.Arch[i][0]) + "#"+repr(self.Arch[i][1])+"#"+repr(self.Arch[i][2])+"\n")
        for i in range(8,12):
            temp += (repr(self.Arch[i][0]) + "#"+repr(self.Arch[i][1])+"\n")
        return temp
        #print (self.Arch)
