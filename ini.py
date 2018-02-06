#Kaiser's ini parser
# Initiate with 
# variable = iniParse(path_to_ini, optional header string)
# then just use variable.function()

class iniParse:
	def __init__(self, path, header = ""):
		self.path = path
		self.header = header
		if self.header != "":
			self.header = "["+header+"]"
		
	def getFull(self):
		with open(self.path, 'r+') as f:

			self.filecontent = f.read()
			f.close()
			return self.filecontent
		
	def findLabel(self, label):
		fl = []
		
		with open(self.path, 'r+') as f:
			fl = f.readlines()
			for line in fl:
				if line.lower().startswith(label.lower()):
					f.close()
					return line[len(label)+1:]
	
	def addLine(self, label, newvalue):
		with open(self.path, 'a') as f:
			f.writelines(label+"="+newvalue)
	
	def delLine(self, label):
		fl = []
		newline = ""
		lin = -1
		with open(self.path, 'r+') as f:
			fl = f.readlines()
			for line in fl:
				lin += 1
				if line.lower().startswith(label.lower()):
					fl[lin] = ""

					
		with open(self.path, 'w+') as f:				
			f.writelines(fl)
			f.close()
			
	def editLine(self, label, newvalue):
		fl = []
		newline = ""
		lin = -1
		with open(self.path, 'r+') as f:
			fl = f.readlines()
			for line in fl:
				lin += 1
				if line.lower().startswith(label.lower()):
					fl[lin] = label+"="+newvalue+"\n"

					
		with open(self.path, 'w+') as f:				
			f.writelines(fl)

			f.close()
			return newline
