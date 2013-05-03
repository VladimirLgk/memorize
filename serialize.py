import sys
import codecs

sys.path.append("e:\data\python");
from knowledge import Knowledge

class Serialize:
	def __init__(self, storage_, dataPath=u'e:\\memorise\\import\\'):
		self.storage = storage_
		self.file_path = dataPath
		
	def importFile(self, name):
		if(len(name) == 0):
			return
		filename=self.file_path+name
		f = codecs.open(filename, "r", "UTF-8")
		listOfWords = f.readlines()
		counter = 0
		statImportKnowledge = []
		for x in listOfWords:
			x = x.strip()
			known = Knowledge()
			known.restore(x)
			self.storage.setKnowledge(kn, statImportKnowledge)
		return statImportKnowledge;	
	
	def exportFile(self, name):
		if(len(name) == 0):
			return
			
		knowledges = self.storage.getAllKnowledges()
		filename=self.file_path+name
		f = codecs.open(filename, "w", "UTF-8") #
		
		for kn in knowledges:	
			text = unicode(kn)+'\n'
			f.write(text)
