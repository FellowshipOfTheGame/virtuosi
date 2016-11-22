#coding: utf-8
import pygame
import time
import math
class Fret:
    px = 0
    origem = 0
    py = 0
    h = 0
    w = 0
    frettipo = 0
    desl = 0
    Nota = None
    clock = 0
    age = 0
    numero = 0
    tam = 1
    def __init__ (self,numero,tipo=1,tam=1):
        self.clock = pygame.time.Clock()
        self.age = 0
        self.frettipo = tipo
        self.py = 0
        self.w = 15
        self.h = 15
        self.tam = tam
        self.accer = 1
        if (numero == 0):
            self.origem = 320
            self.Nota = "verde"
            self.numero = -4.6

        elif (numero == 1):
            self.origem = 337
            self.Nota = "vermelho"
            self.numero = -16.2

        elif (numero == 2):
            self.origem = 352
            self.Nota = "amarelo"
            self.numero = 15.8
        elif (numero == 3):
            self.origem = 367
            self.Nota = "azul"
            self.numero = 4.3
        else:
            self.origem = 345
            self.Nota = None
            self.numero = 0

        self.desl = self.origem
	
    def Move(self):
        self.age += self.clock.tick()
        old_py = self.py
        if self.frettipo == 1:
            self.py = math.pow((self.age+20),1/2)*4+(self.age*self.age*0.00005)
            self.w = int((self.py/500)*50)
            self.h = int((self.py/500)*(32*self.tam))
            #px-px_anterior = dy/m
            self.desl += (self.py - old_py)/self.numero
            self.px =  self.desl - (self.w/2)
        else:
            if (self.py) >= 400:
                if self.tam >1:
                    self.tam /=1.5
                else:
                    self.tam = 1
                self.py = math.pow((self.age+20),1/2)*4+(self.age*self.age*0.00005) + ( self.h -int((self.py/500)*(32+self.tam)))
                self.w = int((self.py/500)*50)
                self.h = int((self.py/500)*(32*self.tam))
                #px-px_anterior = dy/m
                self.desl += (self.py - old_py)/self.numero
                self.px =  self.desl - (self.w/2)
            else:
                self.py = math.pow((self.age+20),1/2)*4+(self.age*self.age*0.00005)
                self.w = int((self.py/500)*50)
                self.h = int((self.py/500)*(32*self.tam))
                #px-px_anterior = dy/m
                self.desl += (self.py - old_py)/self.numero
                self.px =  self.desl - (self.w/2)

    def getTam(self):
        return self.tam
    
    def GetPx(self):
        return self.px

    def GetDrawPy(self):
        if self.frettipo == 1:
            return self.py
        else:
            return (self.py- self.tam)
    
    def GetPy(self):
        return self.py

    def GetTw(self):
        return self.w
    def GetTh(self):
        return self.h

    def GetVe(self):
        return self.accer

    def GetTipo(self):
        return self.frettipo
