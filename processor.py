import e32
import appuifw
import sysinfo
import codecs
import random
import time
import sys
sys.path.append("e:\data\python");

from KnowledgeStorage import KnowledgeStorage
from Knowledge import Knowledge

import_path = u'e:\\memorise\\import\\'
media_path = u'e:\\memorise\\media\\'

class KnowledgeProcessor:
	
	def __init__(self, Storage_):
		self.Storage = Storage_
		self.Knowleges = []
		self.currentKnowledge = -1
			
	def startLearn(self):		
		info = []
		self.Knowleges = self.Storage.getPracticeKnowledges()
		info.append(len(self.Storage))
		print 'There are ', info[0], ' knowledges for repeat'
		
		numNewKnowledges = 0
		if info[0] < maxKnowledge:
			numNewKnowledges = maxKnowledge - info[0]
			
		newKnowledges = self.Storage.getNewKnowledges(numNewKnowledges)	
		info.append(len(newKnowledges))
		print 'There are ', info[1], ' new knowledges'		
		
		Knowleges.extend(newKnowledges)
		print 'There are ', len(lof), ' knowledges for study'
		return info
	
	def getNextKnowledge(self, previousKnowledge):
		nextKnowledge = -1
		generated = 0
		sizeKnowledges = len(self.Knowleges)
		if sizeKnowledges == 1:
			nextKnowledge = 0
		elif sizeKnowledges == 2:
			if previousKnowledge > 1:
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
			self.currentKnowledge = self.getNexKnowledge(self.currentKnowledge)
		know = self.currentKnowledge()
		return know
		
	def currentKnowledge(self):
		know = []
		if len(self.Knowleges) > 0:		
			know.append(unicode(self.Knowleges[self.currentKnowledge].qwest))
			know.append(unicode(self.Knowleges[self.currentKnowledge].answer))
			know.append(self.Knowleges[self.currentKnowledge].suggestion())
		else:
			know.append(u'No knowledegs')
			know.append(u'No knowledegs')
			know.append({})
			currentKnowledge = -1
		know.append(len(self.Knowleges))	
		return know	
	
	def resultKnowledgeRepetition(self, result):	
		if (self.currentKnowledge == -1):
			return 
		
		knowledge = superMemo2Calculation(self.Knowleges[self.currentKnowledge], result)	
		self.Knowleges[self.currentKnowledge] = knowledge
		self.storage.updateOneKnowledge(knowledge)
		
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
			Knowlege.interval = 1
	
		#We don't modify easy factor for new card
		if( not (Knowlege.newCard == 1 and result == 0) ):
			nEasyFactor = Knowlege.easyFactor + (0.1-(5-result)*(0.08+(5-result)*0.02))
			if nEasyFactor < 1.3:
				nEasyFactor = 1.3	
			Knowlege.easyFactor = nEasyFactor
		return Knowlege

	

	

	

	
