import e32
import appuifw
import sysinfo
import codecs
from graphics import *
from key_codes import *
			
def tabs_proc(id):
	print id

def quit():
	app_lock.signal()	
	
	
#def firstMenu():
	

#def showQuwestion():
	

#def showAnswer():

#def getResults():

def onSelect(idx):
	idx = idx

def app0():
	lb = appuifw.Listbox([u'change db',u'import file', u'export'], onSelect)
	appuifw.app.body = lb	
	
def app1():
	text = appuifw.Text()
	ostyle = text.style
	text.style = appuifw.HIGHLIGHT_STANDARD

	text.add(u'n[50], r[11]    	ef[2,7], rep[3]\n')
	text.style = ostyle
	text.add(u'----------------------------------------\n')
	text.add(u'Do you know who those people are\n')
	text.add(u'\n\n\n\n')
	text.add(u'----------------------------------------\n')
	text.bind(EKeySelect, printFact)
	appuifw.app.body = text	
	
def printMenu():
	appuifw.popup_menu([u'easy',u'normal', u'hard', u'unknown']);
	
def printFact():
	te = appuifw.app.body
	te.add(u'Who are those people')
	te.add(u'\n\n\n\n\n\n')
	ostyle = te.style
	te.style = appuifw.HIGHLIGHT_STANDARD
	te.add(u'(1)easy 2, (2)normal 1, (3)hard 1, (*)unknow')
	te.bind(EKeySelect, printMenu)
	appuifw.app.body = te	
	
def app3():
	frm = appuifw.Form([(u'quest','text',u'empty'),(u'answer','text',u'empty')]);
	frm.execute()	

def changeTab(tab_idx):	
	if(tab_idx == 0):
		app0()
			
	if(tab_idx == 1):	
		app1()
		
	if(tab_idx == 2):	
		app3()
		
if __name__ == "__main__":
	
	appuifw.app.title = u"Memorise"  
	appuifw.app.screen = 'full'   
	appuifw.app.exit_key_handler = quit 
	
	tbs = [u'start',u'study',u'cfg']
	appuifw.app.set_tabs(tbs, changeTab)
	appuifw.app.activate_tab(0)
	app0()
	app_lock = e32.Ao_lock()  
	app_lock.wait()
