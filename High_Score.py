#coding: utf-8
class High_Score:
    nome = ""
    recordes = []
    def __init__ (self):
        self.recordes = []
        musics= []
        try:
            file = open ('Data/Musics.vts','r')
            tag = 0
            for i in file:
                aux = 0
                #se encontra a tag
                if (i[0] == "["):
                    try:
                        aux = i.replace('[','')
                        aux = aux.replace(']','')
                        aux = ''.join(aux.split())
                        tag = int(aux)
                        #tag = int(i[1:-2])
                        if (tag > 0):
                            continue
                        else:
                            raise ValueError
                    except ValueError:
                        print ("erro: tag invalida em High_Score.vts")
                #se a tag marca algum opus
                if tag != 0:
                    #adiciona a musica na lista
                    musics.append(''.join(i.split()))
            file.close()
        except IOError:
            sys.exit()
        try:
            file = open ('Data/High_Score.vts','r')
            for i in file:
                #pega os dados do profile
                flag = 0
                ms_nome, score, nome = i.split('#')
                nome = nome[:-1]
                for j in musics:
                    #se a musica da lista esta no arquivo de profile carrega a pontuacao
                    if j == ms_nome:
                        self.recordes.append([ms_nome,int(score),nome])
                        flag = 1
                # se nao achou a musica adiciona nota 0
                """if flag == 0:
                    self.recordes.append([j,0,'Default'])"""
            file.close()
        except IOError:
            if len(self.recordes) == 0:
                for j in musics:
                    self.recordes.append([j,0,'Default'])
            self.save()
    def Get(self):
        return self.recordes
    def Update(self,music_name, score,player_name):
        player_name = ''.join(player_name.split())
        for i in self.recordes:
            if i[0] == music_name:
                if int(i[1]) < score:
                    i[1] = score
                    i[2] = player_name
        self.save()
    def save(self):
        file = open ('Data/High_Score.vts','w')
        for i in self.recordes:
            file.write (i[0]+"#"+repr(i[1])+"#"+i[2]+"\n")
        file.close()
