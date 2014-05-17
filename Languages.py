#coding: utf-8
class Lang:
	nome = ""
	line =[]
	def __init__ (self,arquivo="Default"):
		self.line =[]
		try:
			arquivo = ''.join(arquivo.split())
			file = open ('Data/Lang/'+arquivo+'.vts','r')
			cont =0
			for i in file:
				if cont == 0:
					self.nome = ''.join(i.split())
				else:
					self.line.append(''.join(i.splitlines()))
				cont+=1
			file.close()
		except IOError:
			self.nome = arquivo
			self.save()
	def Get(self,id):
		return self.line[id]
	def save(self):
		self.nome = ''.join(self.nome.split())
		file = open ('Data/Lang/'+self.nome+'.vts','w')
		for i in self.line:
			file.write (i[0])
		file.close()

class Language:
	language = []
	def __init__ (self):
		self.language = []
		self.Load()
	def __init__ (self,lang):
		self.language = []
		self.Load()
		self.MoveUp(lang)
	def GetOne(self):
		return self.language[0]
		
	def GetList(self):
		return self.language
	def GetNameList(self):
		lista = []
		file = open ('Data/Languages.vts','r')
		#file.readline()
		for i in file:
			fl = open ('Data/Lang/'+''.join(i.split())+'.vts','r')
			for j in fl:
				lista.append(j[:-1])
				break
			fl.close()
		file.close()
		return lista
	def MoveUp(self,item):
		lista = []
		file = open ('Data/Languages.vts','r')
		#file.readline()
		for i in file:
			fl = open ('Data/Lang/'+''.join(i.splitlines())+'.vts','r')
			for j in fl:
				#j.replace("\n","")
				if ''.join(j.splitlines()) == item:
					self.language.remove(''.join(i.splitlines()))
					self.language.insert(0,''.join(i.splitlines()))
					break
			fl.close()
		file.close()
		self.Save()
	def RmvOne(self, item):
		flag = 0
		for i in self.language:
			if item == i:
				self.language.remove(item)
	def AddOne(self, item):
		flag = 0
		for i in self.language:
			if item == i:
				flag = 1
		if flag == 0:
			self.language.insert(0,item)
	def Load(self):
		file = open ('Data/Languages.vts','r')
		#file.readline()
		for i in file:
			self.language.append(''.join(i.split()))
		file.close()
	def Save(self):
		file = open ('Data/Languages.vts','w')
		for i in self.language:
			file.write(i+"\n")
		file.close()