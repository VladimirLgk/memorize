import e32
import appuifw
import sysinfo
import codecs
from graphics import *
from key_codes import *

class mainMenu:
	importFile = None
	exportFile = None
	
	def show(self):
		lb = appuifw.Listbox([u'change deck',u'import file', u'export file'], self.onSelect)
		appuifw.app.body = lb
	
	def onSelect(self):
		cur = appuifw.app.body.current()
		if(cur == 2):
			name = appuifw.query(u'Enter file name', 'text')
			self.exportFile(name)
		
class studyScreen:
	def __init__(self, nextKnowledge = None, repetitionResult = None, startLearnCb = None ):
		self.getNextKnowledge = nextKnowledge
		self.setRepetitionResult = repetitionResult
		self.startLearn = startLearnCb
		self.easyInfo = ""
		self.normalInfo = ""
		self.hardInfo = ""

	def show(self):
		self.startLearn()
		self.request()
		
	def request(self):
		text = appuifw.Text()
		ostyle = text.style
		text.style = appuifw.HIGHLIGHT_STANDARD
		if(self.getNextKnowledge):
			kn = self.getNextKnowledge()
			predict = kn[2]
			self.requestText = kn[0]
			self.responceText = kn[1]
			if(len(predict) > 0):	
				text.add(unicode("%d %.1f %d\n" % (kn[3], predict['easyFactor'], predict['rep'])))
				self.easyInfo = unicode(" %d" % (predict['easy']))
				self.normalInfo = unicode(" %d" % (predict['normal']))
				self.hardInfo = unicode(" %d" % (predict['hard']))

		text.style = ostyle
		text.add(u'----------------------------------------\n')
		text.add(u'\n\n')
		text.add(self.requestText)
		text.add(u'\n\n')
		text.add(u'----------------------------------------\n')
		text.bind(EKeySelect, self.responce)
		appuifw.app.body = text	
		
	def responce(self):
		te = appuifw.app.body
		te.add(u'\n\n')
		te.add(self.responceText)
		te.add(u'\n\n\n\n')
		ostyle = te.style
		te.style = appuifw.HIGHLIGHT_STANDARD
		str_info = u'[1 easy]' + self.easyInfo + u'  [2 normal]' + self.normalInfo + u'  [3 hard]' + self.hardInfo + '  [* unknown]'
		te.add(str_info)
		te.bind(EKeySelect, self.resultMenu)
		appuifw.app.body = te	
		
	def resultMenu(self):
		appuifw.popup_menu([u'easy',u'normal', u'hard', u'unknown']);		
	
class editKnowledge:	
	def show(self):
		frm = appuifw.Form([(u'quest','text',u'empty'),(u'answer','text',u'empty')]);
		frm.execute()	

class MemorizeUi:
	def __init__(self, title, quit_cb):
		appuifw.app.title = title  
		appuifw.app.screen = 'full'   
		appuifw.app.exit_key_handler = quit_cb 
		
		self.study = studyScreen()
		self.main = mainMenu()
		self.edit = editKnowledge()
		
		tbs = [u'start',u'study',u'cfg']
		appuifw.app.set_tabs(tbs, self.changeTab)
		self.main.show()
		
	def setStudyCallback(self, nextKnowledge, repetitionResult, startLearnCb):
		self.study.getNextKnowledge = nextKnowledge
		self.study.setRepetitionResult = repetitionResult
		self.study.startLearn =	startLearnCb
		
	def setFileCallback(self, importFile, exportDate):
		self.main.importFile = importFile
		self.main.exportFile = exportDate
				
	def changeTab(self, tab_idx):	
		if(tab_idx == 0):
			self.main.show()
		if(tab_idx == 1):	
			self.study.show()		
		if(tab_idx == 2):	
			self.edit.show()
		
