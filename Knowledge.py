class Knowledge:      
	
	def __init__(self, qwest_, answer_):
		self.id_ = 0
		self.qwest = qwest_
		self.answer = answer_
		self.repetition = 0
		self.easyFactor = 0
		self.interval = 0
		self.showDate = 0
		self.learned = 0
		self.newCard = 0
		self.startDate = ""
		
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
