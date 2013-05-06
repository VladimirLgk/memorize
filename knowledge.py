class Knowledge:      
	
	def __init__(self, qwest_="", answer_=""):
		self.id_ = -1
		self.qwest = qwest_
		self.answer = answer_
		self.repetition = 0
		self.easyFactor = 2.5
		self.interval = 0
		self.showDate = u'01-01-1970'
		self.learned = 0
		self.newCard = 1
		self.startDate = u'01-01-1970'
		
	def __str__(self):
		return "%d;%s;%s;%f;%d;%d;%s;%s;%d"%(self.id_,\
		 self.qwest,\
		 self.answer,\
		 self.easyFactor,\
		 self.repetition,\
		 self.interval,\
		 self.showDate,\
		 self.startDate,\
		 self.newCard)	
		
	def restore(self, str_):
		dataList = str_.split(';')
		#possible sound will passed as third parameter
		if(len(dataList) <= 3):
			self.qwest = dataList[0]
			self.answer = dataList[1]
		elif(len(dataList) == 9):	
			self.id_ = int(dataList[0])
			self.qwest = dataList[1]
			self.answer = dataList[2]
			self.easyFactor = float(dataList[3])
			self.repetition = int(dataList[4])
			self.interval = int(dataList[5])
			if(len(dataList[7]) == 10):
				self.startDate = dataList[7]
				
			if(len(dataList[6]) == 10):
				self.showDate = dataList[6]
				
			self.newCard = int(dataList[8])
			
	def days(self, result, nextShow):
		nEasyFactor = self.easyFactor + (0.1-(5-result)*(0.08+(5-result)*0.02))
		if nEasyFactor < 1.3:
			nEasyFactor = 1.3
		return int(nextShow * nEasyFactor)	

	def suggestion(self):
		result = {}
		result['easyFactor'] = self.easyFactor
		if(self.repetition == 0):
			result['rep'] = 0
			result['easy'] = 0
			result['normal'] = 0
			result['hard'] = 0
		else:
			if(self.interval == 0):
				nextShow = 1
			else:	
				nextShow = self.interval
			result['rep'] = self.repetition
			result['easy'] = self.days(5,nextShow)
			result['normal'] = self.days(4, nextShow)
			result['hard'] = self.days(3, nextShow)
			
		return result			
		
if __name__ == "__main__":

	kn = Knowledge(u'hello',u'world')
	kn.id_ = 17
	kn.easyFactor = 3.4
	kn.repetition = 3
	kn.interval = 5
	kn.startDate = u'10-10-13'
	kn.showDate = u'11-11-13'
	kn.newCard = 1
	
	stringRepr = str(kn)
	
	kn0 = Knowledge()
	kn0.restore(stringRepr)
	
	stringRepr0 = str(kn0)
	
	if(stringRepr != stringRepr0):
		print u'error strings are different\n'
		print 'first: ',stringRepr,'\n'
		print 'second: ',stringRepr0,'\n'
	else:	
		print u'OK strings are identical\n'
