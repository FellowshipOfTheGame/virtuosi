#coding: utf-8
import sys
class Config:
    nivel = 0
    audio = 1.0
    fullscreen = 0
    lang=""
    def __init__ (self,nivel=2,audio=1.0,full=0,language="Portugues Brasileiro"):
        self.nivel = nivel
        self.audio = audio
        self.fullscreen = full
        self.lang = language
    def Return_Config (self):
        return self.nivel, self.audio, self.fullscreen, self.lang
    
    def Get_full(self):
        return self.fullscreen
            
    def Get_lvl(self):
        return self.nivel
    
    def Get_audio(self):
        return float(self.audio)
            
    def Get_lang(self):
        return self.lang
    
    def Set(self, lvl=2, audio=1.0, full=0,language="Portugues Brasileiro"):
        if (lvl in [1,2,5,10]):
            self.nivel = lvl
        else:
            self.nivel = 2
        if (audio >= 0.0) and (audio<=1.0):
            self.audio = audio
        else:
            self.audio = 1.0
        self.fullscreen = full
        self.lang = language
