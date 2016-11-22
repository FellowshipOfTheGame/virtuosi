import subprocess
import os
import platform
import time
class Generate:
    stdi = ''
    Sistemas = {'Windows':'Data/MidiCsv/Windows/midicsv.exe','Darwin':'Data/MidiCsv/Mac/midicsv','Linux':'Data/MidiCsv/Linux/midicsv','Unix':'Data/MidiCsv/Linux/midicsv'}
    #How to Use ('musicname.mid')
    def __init__ (self, stdi):
        print(stdi)
        self.stdi = stdi

    def generateit(self):
        print(platform.system())
        print(self.Sistemas[platform.system()])
        time.sleep(2);
        proc = subprocess.Popen([self.Sistemas[platform.system()], 'Data/Musics/'+self.stdi+'.mid'], stdout=subprocess.PIPE, shell=False)
        stdout_value = str(proc.communicate()[0])
        f = open ('stdout_value.txt','w')
        f.write(stdout_value)
        f.close()
        if stdout_value == None:
            print("Problemas ocorreram no gerador de CSV, verifique o nome da musica que lhe foi passada ou se a classe esta funcional.")
        """aux = ''
        for i in stdout_value:
            aux +=str(i)
        aux = aux[2:-1]
        f = open ('saida2.txt','w')
        f.write(aux)
        f.close()"""
        #print("-"+stdout_value+"-")
        return stdout_value
        #print("-"+stdout_value+"-")
