#class Screen
#class FirstScreen
#class RequestScreen
#class AnswerScreen
			
					 
class RemindUi(BaseUi):
	INIT_STAGE=1
	START_STAGE=2
	SHOW_FACT_STAGE=3
	SHOW_ANSWER_STAGE=4

	currentStage = INIT_STAGE
	selectedElement = 0
	
	def __init__(self,importFileCb=None,nextFactCb=None, factResultCb=None ):
		
		self.importFileCb = importFileCb
		self.nextFactCb = nextFactCb
		self.factResultCb = factResultCb
		
		BaseUi.__init__(self)
			
		self.knownFact = Label(u'good',(5,10),(280,90),self.widgets)
		self.unknownFact = Label(u'bad',(5,105),(280,90),self.widgets)
		
		self.showAnswer = Button(u'show answer', (110,205),(90,25),self.widgets)	
		self.showAnswer.apperance(0x0,(0,208,128),1)
		
		self.easyButton = Button(u'easy', (20,205),(50,25),self.widgets)	
		self.easyButton.apperance(0x0,(0,208,128),1)	
	
		self.normalButton = Button(u'normal', (75,205),(50,25),self.widgets)	
		self.normalButton.apperance(0x0,(0,208,128),1)
	
		self.hardButton = Button(u'hard', (130,205),(50,25),self.widgets)	
		self.hardButton.apperance(0x0,(0,208,128),1)
		
		self.failButton = Button(u'unknown', (185,205),(70,25),self.widgets)	
		self.failButton.apperance(0x0,(0,208,128),1)
		
		
		self.learnCount = Label(u'0', (270,205),(30,25),self.widgets)	
		
		self.startLearnBtn = Button(u'start learn', (110,90),(90,25),self.widgets)	
		self.startLearnBtn.apperance(0x0,(0,208,128),1)
		
		self.importFileBtn = Button(u'import file', (110,120),(90,25),self.widgets)	
		self.importFileBtn.apperance(0x0,(0,208,128),1)
		self.startStage()
		
	def startStage(self):
		self.importFileBtn.visible = 1	
		self.startLearnBtn.visible = 1
		self.startLearnBtn.active = 1
		self.currentStage = self.START_STAGE
		
	def showFactStage(self):
		if(self.nextFactCb):
			fact = self.nextFactCb()
			self.knownFact.text = fact[0]
			self.unknownFact.text = fact[1]
			self.learnCount.text =  unicode("%d" % (fact[2]))
		self.knownFact.visible = 1
		self.showAnswer.visible = 1
		self.learnCount.visible = 1
		self.showAnswer.active = 1
		self.currentStage = self.SHOW_FACT_STAGE
		
	def showAnswerStage(self):
		self.unknownFact.visible = 1		
		self.easyButton.visible = 1
		self.normalButton.visible = 1
		self.hardButton.visible = 1
		self.failButton.visible = 1
		
		self.easyButton.active = 1
		self.currentStage = self.SHOW_ANSWER_STAGE
		
	def clearFactStage(self):
		self.showAnswer.visible = 0		
		
	def clearAnswerStage(self):
		self.knownFact.visible = 0
		self.unknownFact.visible = 0		
		
		self.easyButton.visible = 0
		self.normalButton.visible = 0
		self.hardButton.visible = 0
		self.failButton.visible = 0	

	def clearStartStage(self):
		self.importFileBtn.visible = 0	
		self.startLearnBtn.visible = 0
			
	def pressSelectedButton(self):
		if(self.currentStage == self.START_STAGE):
			self.clearStartStage()
			if(self.startLearnBtn.active):
				self.showFactStage()
			if(self.importFileBtn.active):
				if(self.importFileCb):
					self.importFileCb()
				self.startStage()			
		elif (self.currentStage == self.SHOW_FACT_STAGE):
			self.clearFactStage()
			self.showAnswerStage()
		elif (self.currentStage == self.SHOW_ANSWER_STAGE):
			if(self.factResultCb):
				self.factResultCb(self.getAnswerResult())
			self.clearAnswerStage()
			self.showFactStage()
			
	def getAnswerResult(self):
		if(self.easyButton.active):
			self.easyButton.active = 0
			return 3;
		elif(self.normalButton.active):
			self.normalButton.active = 0
			return 2;	
		elif(self.hardButton.active):
			self.hardButton.active = 0
			return 1;
		elif(self.failButton.active):
			self.failButton.active = 0
			return 0;
		return -1;	
			
	def selectNextVButton(self):
		if(self.currentStage == self.START_STAGE):	
			if(self.importFileBtn.active):
				self.startLearnBtn.active = 1
				self.importFileBtn.active = 0
			elif(self.startLearnBtn.active):
				self.startLearnBtn.active = 0
				self.importFileBtn.active = 1
				
	def selectPrevVButton(self):
		self.selectNextVButton()
		
	def selectNextHButton(self):
		if(self.currentStage == self.SHOW_ANSWER_STAGE):
			if(self.easyButton.active):
				self.easyButton.active = 0
				self.normalButton.active = 1
				self.hardButton.active = 0
				self.failButton.active = 0
			elif(self.normalButton.active):
				self.easyButton.active = 0
				self.normalButton.active = 0
				self.hardButton.active = 1
				self.failButton.active = 0
			elif(self.hardButton.active):
				self.easyButton.active = 0
				self.normalButton.active = 0
				self.hardButton.active = 0
				self.failButton.active = 1
			elif(self.failButton.active):
				self.easyButton.active = 1
				self.normalButton.active = 0
				self.hardButton.active = 0
				self.failButton.active = 0	
				
	def selectPreviousHButton(self):
		self.selectNextHButton()
							
if __name__ == "__main__":
	AppUi = RemindUi()
	AppUi.nextStage()	
	AppUi.nextStage()
	AppUi.nextStage()

	print 'App ui system has ',len(AppUi.widgets),'widgets'	