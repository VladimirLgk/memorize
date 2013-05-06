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
		lb = appuifw.Listbox([u'change db',u'import file', u'export file'], self.onSelect)
		appuifw.app.body = lb
	
	def onSelect(self):
		cur = appuifw.app.body.current()
		if(cur == 2):
			name = appuifw.query(u'Enter file name', 'text')
			self.exportFile(name)
		elif(cur == 1):
			name = appuifw.query(u'Enter file name', 'text')
			kstat = self.importFile(name)
			sstat = u'upd %d, new %d'%(kstat[0], kstat[1])
			appuifw.note(sstat)
		elif(cur == 0):
			name = appuifw.query(u'Enter deck name', 'text')	
			self.openDatabase(name)
			
class studyScreen:
	wichDatabase = None
	
	def __init__(self, nextKnowledge = None, repetitionResult = None, startLearnCb = None ):
		self.getNextKnowledge = nextKnowledge
		self.setRepetitionResult = repetitionResult
		self.startLearn = startLearnCb
		self.easyInfo = ""
		self.normalInfo = ""
		self.hardInfo = ""

	def show(self):
		self.request(self.startLearn())
		
	def request(self, linfo):
		sinfo =	u'd[%s] '%(self.wichDatabase())
		#first initial inforamtion 
		if(len(linfo) > 0):
			sinfo = sinfo+u' \tr%d, n%d'%(linfo[0], linfo[1])
			
		text = appuifw.Text()
		ostyle = text.style
		text.style = appuifw.HIGHLIGHT_STANDARD
		if(self.getNextKnowledge):
			kn = self.getNextKnowledge()
			predict = kn[2]
			self.requestText = kn[0]
			self.responceText = kn[1]
			if(len(predict) > 0):	
				sinfo = sinfo+u'\tk%d r%d %.1f'%(kn[3], predict['easyFactor'], predict['rep'])
				self.easyInfo = unicode("%d"%(predict['easy']))
				self.normalInfo = unicode("%d"%(predict['normal']))
				self.hardInfo = unicode("%d"%(predict['hard']))
		sinfo = sinfo + u'\n'		
		text.add(sinfo)
		text.style = ostyle
		text.add(u'\n')
		text.add(u'\n')
		text.add(self.requestText)
		text.add(u'\n')
		text.add(u'\n')
		text.bind(EKeySelect, self.responce)
		appuifw.app.body = text	
		
	def responce(self):
		te = appuifw.app.body
		te.add(u'\n')
		te.add(self.responceText)
		te.add(u'\n')
		te.add(u'\n')
		te.add(u'\n')
		ostyle = te.style
		te.style = appuifw.HIGHLIGHT_STANDARD
		str_info = u'[1]easy ' + self.easyInfo + u'  [2]normal ' + self.normalInfo + u'  [3]hard ' + self.hardInfo + '  [*]unkn'
		te.add(str_info)
		te.bind(EKeySelect, self.resultMenu)
		appuifw.app.body = te	
		
	def resultMenu(self):
		resultMenu = appuifw.popup_menu([u'easy',u'normal', u'hard', u'unknown']);
		
		if resultMenu == 3:
			self.setRepetitionResult(0)
		else:	
			#revers: easy-5, normal-4, hard-3
			self.setRepetitionResult(5-resultMenu)
		self.request([])
		
	
class editKnowledge:
	getKnowledge = None	
	storeKnowledge = None
	def show(self):
		kn = self.getKnowledge()
		frm = appuifw.Form([(u'quest','text',kn[0]),(u'answer','text',kn[1])]);
		frm.save_hook = self.saveKnowledge
		frm.execute()
		
	def saveKnowledge(self, knowledge):
		requestList = knowledge[0]
		answerList = knowledge[1]
		know = [unicode(requestList[2]),unicode(answerList[2])]
		self.storeKnowledge(know)
		return True

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
		
	def setStudyCallback(self, nextKnowledge, repetitionResult, startLearnCb):
		self.study.getNextKnowledge = nextKnowledge
		self.study.setRepetitionResult = repetitionResult
		self.study.startLearn =	startLearnCb
		
	def setFileCallback(self, importFile, exportDate):
		self.main.importFile = importFile
		self.main.exportFile = exportDate
		
	def setDatabaseCallback(self, openDatabase, wichDatabase):
		self.main.openDatabase = openDatabase
		self.study.wichDatabase = wichDatabase
		
	def setEditCallback(self, getKnowledge, storeKnowledge):
		self.edit.getKnowledge = getKnowledge
		self.edit.storeKnowledge = storeKnowledge	
				
	def changeTab(self, tab_idx):	
		if(tab_idx == 0):
			self.main.show()
		if(tab_idx == 1):	
			self.study.show()		
		if(tab_idx == 2):	
			self.edit.show()
		
