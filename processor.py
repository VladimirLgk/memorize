import e32
import appuifw
import sysinfo
import codecs
import random
import time
import sys

sys.path.append("e:\data\python");
from storage import KnowledgeStorage
from knowledge import Knowledge

import_path = u'e:\\memorise\\import\\'
media_path = u'e:\\memorise\\media\\'

class KnowledgeProcessor:
	
	def __init__(self, Storage_):
		self.Storage = Storage_
		self.Knowleges = []
		self.currentKnowledge = -1
		self.maxKnowledge = 60
		
	def startLearn(self):		
		info = []
		self.Knowleges = self.Storage.getPracticeKnowledges()
		info.append(len(self.Knowleges))
		#print 'There are ', info[0], ' knowledges for repeat'
		
		numNewKnowledges = 0
		if info[0] < self.maxKnowledge:
			numNewKnowledges = self.maxKnowledge - info[0]
			
		newKnowledges = self.Storage.getNewKnowledges(numNewKnowledges)	
		info.append(len(newKnowledges))
		#print 'There are ', info[1], ' new knowledges'		
		
		self.Knowleges.extend(newKnowledges)
		#print 'There are ', info[0] + info[1],' knowledges for study'
		return info
	
	def getNextKnowledge(self, previousKnowledge):
		nextKnowledge = -1
		generated = 0
		sizeKnowledges = len(self.Knowleges)
		if sizeKnowledges == 1:
			nextKnowledge = 0
		elif sizeKnowledges == 2:
			if previousKnowledge > 1 or previousKnowledge < 0:
				previousKnowledge = 1
			nextKnowledge = 1 - previousKnowledge
		else:	
			newValue = 0
			while( not newValue):		
				nextKnowledge = random.randrange(0, sizeKnowledges, 1)
				if(nextKnowledge != previousKnowledge):
					newValue = 1
		return nextKnowledge
	
	def nextKnowledge(self):
		if len(self.Knowleges) > 0:
			self.currentKnowledge = self.getNextKnowledge(self.currentKnowledge)
		return self.getCurrentKnowledge()
		
	def getCurrentKnowledge(self):
		kn = []
		if len(self.Knowleges) > 0 and self.currentKnowledge != -1 :		
			kn.append(unicode(self.Knowleges[self.currentKnowledge].qwest))
			kn.append(unicode(self.Knowleges[self.currentKnowledge].answer))
			kn.append(self.Knowleges[self.currentKnowledge].suggestion())
		else:
			kn.append(u'No knowledegs')
			kn.append(u'No knowledegs')
			kn.append({})
			currentKnowledge = -1
			
		kn.append(len(self.Knowleges))	
		return kn	
	
	def setCurrentKnowledge(kn):
		if len(self.Knowleges) > 0 and self.currentKnowledge != -1:
			self.Knowleges[self.currentKnowledge].qwest = kn[0]	
			self.Knowleges[self.currentKnowledge].answer = kn[1]
			knowledge = self.Knowleges[self.currentKnowledge]	
			self.Storage.updateExistKnowledge(knowledge)
	
	def resultKnowledgeRepetition(self, result):	
		if (self.currentKnowledge == -1):
			return 
		
		knowledge = self.superMemo2Calculation(self.Knowleges[self.currentKnowledge], result)	
		self.Knowleges[self.currentKnowledge] = knowledge
		self.Storage.updateRepetitionKnowledge(knowledge)
		
		if(knowledge.repetition > 1):
			del self.Knowleges[self.currentKnowledge]
	
	#TODO: make this as configurable property 
	def superMemo2Calculation(self, Knowlege, result):
		if(result != 0):
			if(Knowlege.repetition == 0):
				Knowlege.interval = 0
				Knowlege.repetition = 1
			elif(Knowlege.repetition == 1):
				Knowlege.interval = 1
				Knowlege.repetition = 2
				Knowlege.newCard = 0 
			else:
				Knowlege.repetition += 1
				Knowlege.interval = int(Knowlege.interval*Knowlege.easyFactor)
		else:		
			Knowlege.repetition = 0
			Knowlege.interval = 0
	
		#We don't modify easy factor for new card
		if( not (Knowlege.newCard == 1 and result == 0) ):
			nEasyFactor = Knowlege.easyFactor + (0.1-(5-result)*(0.08+(5-result)*0.02))
			if nEasyFactor < 1.3:
				nEasyFactor = 1.3	
			Knowlege.easyFactor = nEasyFactor
		return Knowlege

	

	

	

	
