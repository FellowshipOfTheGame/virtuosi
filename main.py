#coding: utf-8
__authors__ = "Helder S. L. Moraes, Marcelo 'Esquilo', Ricardo 'Buda' Fuzeto ...."
__copyright__ = ""
__credits__ = ["Helder S. L. Moraes", "Alexis Kiosia", "Ricardo Fuzeto","Ana Luiza","Ricardo Fuzeto","..."]
__license__ = "..."
__version__ = "1.6"
__maintainer__ = "Helder S. L. Moraes"
__email__ = "helderslmoraes@yahoo.com.br"
__status__ = "Developing"
# http://en.wikipedia.org/wiki/List_of_MIDI_editors_and_sequencers
# http://en.wikipedia.org/wiki/MIDI_Show_Control
# http://home.roadrunner.com/~jgglatt/tutr/miditutr.5htm
# http://www.midi.org/techspecs/midimessages.php
# http://stackoverflow.com/questions/3850688/reading-midi-files-in-java
# http://jmusic.ci.qut.edu.au/jmtutorial/ReadUseMIDI.ht5ml

#http://www.fourmilab.ch/webtools/midicsv/
#http://docs.python.org/library/subprocess.html
#http://stackoverflow.com/questions/1811691/running-an-outside-program-executable-in-python

import pygame
import cProfile
from Virtuosi import *
from Extras import *
from Config import *
import time

def main():
    #Preparacao da tela
    pygame.init()
    #TORNA O MOUSE INVISIVEL
    pygame.mouse.set_cursor((8,8),(0,0),(1,1,1,1,1,1,1,1),(1,1,1,1,1,1,1,1))
    
    resolucao = (800, 600)
    #carrega configuracao padrao
    config = Config ()
    #TENTA CARREGAR UM PROFILE
    try:
        prof = Profiles()
        prof.Load()
        profile = Profile(prof.GetOne())
        #CARREGA CONFIGURACAO DO PROFILE
        config = profile.Return_Config()
        if config.Get_full() == 1:
            tela = pygame.display.set_mode(resolucao, pygame.FULLSCREEN)
        else:
            tela = pygame.display.set_mode(resolucao)
    except IOError:    
        tela = pygame.display.set_mode(resolucao, pygame.FULLSCREEN)
    
    pygame.display.set_caption("Virtuosi!")
    video = pygame.movie.Movie("Graphics/Movies/Virtuosi.mpg")
    video.set_display(tela,((0,0),resolucao))

    video.play()
    video.set_volume(1)
    while (video.get_busy()):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                video.stop()
    Virt = Virtuosi(tela)
    #Loop de Execucao
    rodando = True
    while rodando:
        #EVENTO DE TERMINO DO PROGRAMA
        rodando = Virt.Menu_P()
    pygame.quit()

if __name__ == "__main__":
    #cProfile.run("main()")
    main()
