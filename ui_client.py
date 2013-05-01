import e32
import appuifw
import sysinfo
import codecs
from graphics import *
from key_codes import *
import random
import time
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
new_card=10
max_card=60					

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
		x = x.strip()
		knowns = x.split(';',2)
		#print "request: ", knowns[0]
		#print "answer: ", knowns[1]
		db.insertKnowns(knowns[0], knowns[1],0)
	#print "read strings", counter
	lof = db.getPracticeFacts()
	return counter;
	
def days(fact,result, nextShow):
	nEasyFactor = fact.easyFactor + (0.1-(5-result)*(0.08+(5-result)*0.02))
	if nEasyFactor < 1.3:
			nEasyFactor = 1.3
	return int(nextShow * nEasyFactor)		
	
def suggestion(fact):
	result = {}
	result['easyFactor'] = fact.easyFactor
	if(fact.repetition == 0):
		result['rep'] = 0
		result['easy'] = 0
		result['normal'] = 0
		result['hard'] = 0
	else:
		if(fact.interval == 0):
			nextShow = 1
		else:	
			nextShow = fact.interval
		
		result['rep'] = fact.repetition
		result['easy'] = days(fact,5,nextShow)
		result['normal'] = days(fact,4, nextShow)
		result['hard'] = days(fact,3, nextShow)
	return result
	
def getNextFact(previousFact):
	nextFact = -1
	generated = 0
	if len(lof) == 1:
		nextFact = 0
	elif len(lof) == 2:
		if previousFact > 1:
			previousFact = 1
		nextFact = 1 - previousFact
	else:	
		newValue = 0
		while( not newValue):		
			nextFact = random.randrange(0, len(lof), 1)
			if(nextFact != previousFact):
				newValue = 1
	return nextFact
	
def nextFact():
	fact = []
	global currentFact
	if len(lof) > 0:
		currentFact = getNextFact(currentFact)
					
		fact.append(unicode(lof[currentFact].qwest))
		fact.append(unicode(lof[currentFact].answer))
		fact.append(suggestion(lof[currentFact]))
	else:
		fact.append(u'All learned')
		fact.append(u'All learned')
		fact.append({})
		currentFact = -1
	fact.append(len(lof))	
	return fact
	

def superMemo2Calculation(fact, result):
	if(result != 0):
		if(fact.repetition == 0):
			fact.interval = 0
			fact.repetition = 1
		elif(fact.repetition == 1):
			fact.interval = 1
			fact.repetition = 2
			fact.newCard = 0 
		else:
			fact.repetition += 1
			fact.interval = int(fact.interval*fact.easyFactor)
	else:		
		fact.repetition = 0
		fact.interval = 1
	
	#We don't modify easy factor for new card
	if( not (fact.newCard == 1 and result == 0) ):
		nEasyFactor = fact.easyFactor + (0.1-(5-result)*(0.08+(5-result)*0.02))
		if nEasyFactor < 1.3:
			nEasyFactor = 1.3	
		fact.easyFactor = nEasyFactor
		
	return fact
		
def factRepetitionResult(result):	
	global currentFact
	if (currentFact == -1):
		return 
		
	fact = superMemo2Calculation(lof[currentFact], result)	
	lof[currentFact] = fact
	db.storeFact(fact)
	if(fact.repetition > 1):
		del lof[currentFact]
			
def startLearn():
	global lof			
	info = []
	lof = db.getPracticeFacts()
	print 'There are ', len(lof), ' facts for repeat'
	
	info.append(len(lof))
	requestNewCard = 0
	if len(lof) < max_card:
		requestNewCard = max_card - len(lof)
	newFacts = db.getNewFacts(requestNewCard)	
	info.append(len(newFacts))
	print 'There are ', len(newFacts), ' new facts'		
	lof.extend(newFacts)
	print 'There are ', len(lof), ' facts for study'
	return info

if __name__ == "__main__":
	
	appuifw.app.title = u"Memorise"  
	appuifw.app.screen = 'full'   
	appuifw.app.exit_key_handler = quit 
	random.seed()
	
	db = memdb()
	
	stInfo = startLearn()
	
	AppUi = RemindUi(importFile, nextFact, factRepetitionResult)
	AppUi.setInfo(stInfo)
	
	cnv = appuifw.Canvas(event_callback=handle_event, redraw_callback=handle_redraw)
	img = Image.new(cnv.size)
	
	appuifw.app.body = cnv

	app_lock = e32.Ao_lock()  
	app_lock.wait()


