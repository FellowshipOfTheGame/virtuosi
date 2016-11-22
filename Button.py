#coding: utf-8
import pygame
import threading
import time
import math

class Button:
    image = None
    tela = None
    control = 0
    def __init__ (self, img):
        self.control = 0
        self.image = img

    def getState(self):
        if self.control!=0:
            return True
        else: 
            return False
    
    def click(self):
        self.control == 1
    def desenha(self):
        if self.image == 0:
            if self.control == 0:
                return pygame.image.load("Graphics/Buttons/botao.jpg")
            else:
                self.control = 0
                return pygame.image.load("Graphics/Buttons/botao_press.jpg")
        else:
            if self.control == 0:
                return pygame.image.load("Graphics/Buttons/botao_red.png")
            else:
                self.control = 0
                return pygame.image.load("Graphics/Buttons/botao_red_press.png")
