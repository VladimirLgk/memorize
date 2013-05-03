class Knowledge:      
	
	def __init__(self, qwest_="", answer_=""):
		self.id_ = -1
		self.qwest = qwest_
		self.answer = answer_
		self.repetition = 0
		self.easyFactor = 0
		self.interval = 0
		self.showDate = ""
		self.learned = 0
		self.newCard = 0
		self.startDate = ""
		
	def __str__(self):
		return "%d;%s;%s;%f;%d;%d;%s;%s;%d"%(self.id_, self.qwest, self.answer, self.easyFactor,\
						self.repetition,self.interval,self.startDate, self.showDate, self.newCard)	
		
	def fullRestore(self, str_):
		dataList = str_.split(';')
		self.id_ = dataList[0]
		self.qwest = dataList[1]
		self.answer = dataList[2]
		self.easyFactor = dataList[3]
		self.repetition = dataList[4]
		self.interval = dataList[5]
		self.startDate = dataList[6]
		self.showDate = dataList[7]
		self.newCard = dataList[8]
		self.learned = 0
		
			
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
