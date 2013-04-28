import e32
import appuifw
from key_codes import *
import sysinfo
from graphics import *


class Label:
	CENTER_ALIGN = 1
	TR_ALIGN = 2
	width = 1
	aflag = CENTER_ALIGN
	visible = 0
	
	def __init__(self,text_, pos_, size_, container=None):	
		self.text = text_
		self.pos = pos_
		self.size = size_
		self.exText = ''
		if(container != None):
			container.append(self)
		
	def area(self, pos_, siz_):
		self.pos = pos_
		self.size = siz_
	
	def font(self, ftype, fsize):
		self.fntSize = fsize
		self.fntType = ftype 
	
	def text(self, text_, align_):
		self.text = text_
		self.aflag = align_

	def apperance(self, outline_, fill_, width_):	
		self.outline = outline_
		self.fill = fill_
		self.width = width_
			
	def draw(self, img_):
		if (self.visible != 0):
			text_pos = (self.pos[0]+5,self.pos[1]+18)
			img_.text(text_pos, self.text+self.exText)#, font=(self.fntType,self.fntSize)
		
class Button(Label):
	active = 0
	
	def hotKey(self, hotkey_):	
		self.hotkey = hotkey_
		
	def draw(self, img_):
		if(self.visible != 0):
			width_ = self.width
			if(self.active):
				width_+=2
			img_.rectangle((self.pos[0],self.pos[1], self.pos[0]+self.size[0], self.pos[1]+self.size[1]),fill=self.fill, width=width_, outline=self.outline)
			Label.draw(self, img_)
	
class BaseUi:
	def __init__(self):
		self.widgets = []
		
	def draw(self, img_):
		for widget in self.widgets:
			if(widget.visible != 0):
				widget.draw(img_)
				
	def selectNextHButton():
		return
		
	def selectNextVButton():
		return	
	
	def selectPreviousVButton():
		return	
	
	def selectPreviousHButton():
		return	
	
	def pressSelectedButton():
		return	
	
				
	def pressed_key(self, keycode):
		if keycode == EKeyRightArrow:
			self.selectNextHButton()			
		elif keycode == EKeyLeftArrow:
			self.selectPreviousHButton()
		elif keycode == EKeyUpArrow:
			self.selectNextVButton()			
		elif keycode == EKeyDownArrow:
			self.selectPreviousVButton()	
		elif keycode == EKeySelect:
			self.pressSelectedButton()
								
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
			
		self.knownFact = Label(u'good',(5,15),(280,90),self.widgets)
		self.unknownFact = Label(u'bad',(5,105),(280,90),self.widgets)
		
		self.showAnswer = Button(u'show answer', (110,205),(90,25),self.widgets)	
		self.showAnswer.apperance(0x0,(0,208,128),1)
		
		self.easyButton = Button(u'easy', (5,205),(70,25),self.widgets)	
		self.easyButton.apperance(0x0,(0,208,128),1)	
	
		self.normalButton = Button(u'normal', (80,205),(80,25),self.widgets)	
		self.normalButton.apperance(0x0,(0,208,128),1)
	
		self.hardButton = Button(u'hard', (165,205),(70,25),self.widgets)	
		self.hardButton.apperance(0x0,(0,208,128),1)
		
		self.failButton = Button(u'unknown', (240,205),(70,25),self.widgets)	
		self.failButton.apperance(0x0,(0,208,128),1)
		
		
		self.infoBox = Label(u'0', (240,1),(60,25),self.widgets)	
		
		self.startLearnBtn = Button(u'start learn', (110,90),(90,25),self.widgets)	
		self.startLearnBtn.apperance(0x0,(0,208,128),1)
		
		self.importFileBtn = Button(u'import file', (110,120),(90,25),self.widgets)	
		self.importFileBtn.apperance(0x0,(0,208,128),1)
		self.startStage()
		
	def setInfo(self, stInfo):
		self.infoBox.text = unicode("r %d, n %d" % (stInfo[0], stInfo[1]))	
		
	def startStage(self):
		self.importFileBtn.visible = 1	
		self.infoBox.visible = 1
		self.startLearnBtn.visible = 1
		self.startLearnBtn.active = 1
		self.currentStage = self.START_STAGE
		
	def showFactStage(self):
		if(self.nextFactCb):
			fact = self.nextFactCb()
			predict = fact[2]
			self.knownFact.text = fact[0]
			self.unknownFact.text = fact[1]
			if(len(predict) > 0):	
				self.infoBox.text =  unicode("%d %.1f %d" % (fact[3], predict['easyFactor'], predict['rep']))
				self.easyButton.exText = unicode(" %d" % (predict['easy']))
				self.normalButton.exText = unicode(" %d" % (predict['normal']))
				self.hardButton.exText = unicode(" %d" % (predict['hard']))
			
		self.knownFact.visible = 1
		self.showAnswer.visible = 1
		self.infoBox.visible = 1
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
		self.infoBox.visible = 0
		
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
			return 5;
		elif(self.normalButton.active):
			self.normalButton.active = 0
			return 4;	
		elif(self.hardButton.active):
			self.hardButton.active = 0
			return 3;
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
	

	






