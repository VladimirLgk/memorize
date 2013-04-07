import e32
import appuifw
import sysinfo
import codecs
from graphics import *
from key_codes import *
import random

import sys
sys.path.append("e:\data\python");
from ui import RemindUi
from dbapi import memdb
from dbapi import fact

import_path = u'e:\\memorise\\import\\'
media_path = u'e:\\memorise\\media\\'
			
AppUi = None			
img = None
db = None
lof = []

currentFact = 0

def tabs_proc(id):
	print id

def quit():
	app_lock.signal()	

def handle_redraw(rect):
	SystemRedraw(rect)
	
		
def handle_event(event):
	if event['type'] == appuifw.EEventKey:
		AppUi.pressed_key(event['keycode'])		
	SystemRedraw(((0,0),(0,0)))			
			
def SystemRedraw(rect):
	global ws
	if img:
		img.clear()
		AppUi.draw(img)
		cnv.blit(img)	

def importFile():
	filename=import_path+u'new_word.txt'
	f = codecs.open(filename, "r", "UTF-8")
	listOfWords = f.readlines()
	counter = 0
	for x in listOfWords:
		knowns = x.split(';',2)
		print "request: ", knowns[0]
		print "answer: ", knowns[1]
		db.insertKnowns(knowns[0], knowns[1],0)
	print "read strings", counter
	lof = db.getPracticeFacts()
	return counter;
		
def nextFact():
	fact = []
	global currentFact
	if len(lof) > 0:
		if len(lof) == 1:
			currentFact = 0
		else:		
			currentFact = random.randrange(0, len(lof)-1, 1)
		#print "Next fact ", currentFact, " size of fact ", len(lof), " req: ",unicode(lof[currentFact].qwest)
		fact.append(unicode(lof[currentFact].qwest))
		fact.append(unicode(lof[currentFact].answer))
	else:
		fact.append(u'All learned')
		fact.append(u'All learned')
		currentFact = -1
	fact.append(len(lof))	
	return fact
	
def factRepetitionResult(result):	
	global currentFact
	#print "Result of repetition", result, "currFact: ", currentFact
	if (result > 0) and (currentFact != -1):
		#print "Will deleted fact ", currentFact, " size of fact ", len(lof), " req: ",unicode(lof[currentFact].qwest)
		del lof[currentFact]
			
if __name__ == "__main__":
	
	appuifw.app.title = u"Memorise"  
	appuifw.app.screen = 'full'   
	appuifw.app.exit_key_handler = quit 
	random.seed()
			
	
	db = memdb()
	lof = db.getPracticeFacts()
	print 'Facts in the database', len(lof)
	
	AppUi = RemindUi(importFile, nextFact, factRepetitionResult)
	
	cnv = appuifw.Canvas(event_callback=handle_event, redraw_callback=handle_redraw)
	img = Image.new(cnv.size)
	
	appuifw.app.body = cnv

	app_lock = e32.Ao_lock()  
	app_lock.wait()


