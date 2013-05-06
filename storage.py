import e32
import e32db
import codecs
import appuifw
import key_codes
import zlib
import time
import sys

sys.path.append("e:\data\python");

from knowledge import Knowledge

ID = 1
REQ_DATA = 2
REQ_SND = 3
RESP_DATA = 4
RESP_SND = 5	
EESY_FACTOR = 6
INTERVAL = 7
REPETITION = 8
START_DATE = 9
NEXT_DATE = 10
NEW_CARD = 11

ERR_DUPLICATE_RECORDS = -2
ERR_GETTING_DATA = -3

def getDate(timeValue):
	dateTime = e32db.format_time(timeValue).split()			   
	return dateTime[0]

def SimpleLogger(str):
	print str
				
class KnowledgeStorage:
		
	def __init__(self,filedb, path_, Logger=SimpleLogger):
		self.Log = Logger
		self.db = e32db.Dbms()
		self.dbv = e32db.Db_view()
		self.path = path_
		self.open(filedb)
		
	def	dbName(self):
		return self.fileDb
		
	def open(self, filedb):
		self.fileDb = filedb
		self.dbPath = self.path+filedb
		self.db.close()
		try:
			self.db.open(self.dbPath)
			self.Log("the memorise data base open")
		except:
			self.Log("the memorise data base not found create new")
			self.db.create(self.dbPath)
			self.db.open(self.dbPath)
			self.initNewStorage()
	
	def execQuery(self, query, errorMessage=None):
		try:
			self.db.execute(query )
		except SymbianError:
			self.Log(errorMessage)
			self.Log(sys.exc_info()[0])
			self.Log(sys.exc_info()[1])
			self.Log(sys.exc_info()[2])	
				   
	def initNewStorage(self):
		req = u'create table facts (id counter, reqData varchar(128),reqSound bigint,respData varchar(128),\
			respSound bigint, easyFactor float, interval integer,repetition integer, startDate date, showDate date, newCard integer)'
		self.execQuery(req,"Error create table:")
		
	def	setKnowledge(self, kn, kstat):
		result = self.isKnowledgeExist(kn)
		if(result == 1):
			kstat[0] += 1
			self.updateExistKnowledge(kn)
		elif(result == 0):	
			self.insertNewKnowledge(kn)
			kstat[1] += 1
		else:
			print u'error in find knowledge ',result		

	def isKnowledgeExist(self, kn):
		knReq = u'select * from facts where id = %d'%(kn.id_)
		if(kn.id_ == -1):
			knReq = u'select * from facts where reqData = \'%s\''%(kn.qwest)
		try:
			#print "Select ek:",knReq	
			self.dbv.prepare(self.db,knReq)
			if(self.dbv.count_line() == 0):	
				return 0
			if(self.dbv.count_line() > 1):	
				return ERR_DUPLICATE_RECORDS
			self.dbv.get_line()	
			kn.id_ = self.dbv.col(ID)
			return 1
		except SymbianError:
			self.Log("Error get knowlege: ")
			self.Log(sys.exc_info()[0])
			self.Log(sys.exc_info()[1])
			self.Log(sys.exc_info()[2])
		return ERR_GETTING_DATA
		
	def insertNewKnowledge(self, kn):							
		req = "insert into facts (reqData, reqSound, respData, respSound, easyFactor,\
interval, repetition, startDate, showDate, newCard) \
values ('%s',%d,'%s',%d, %f, %d, %d, #%s#, #%s#, %d)" %\
		(kn.qwest, 0, kn.answer, 0, kn.easyFactor, kn.interval, kn.repetition, kn.startDate, kn.showDate, kn.newCard)	
		#print "Insert nk:",req						
		self.execQuery(unicode(req),"Error insert fact: "+req)		
	
	def updateExistKnowledge(self, kn):
		req = "update facts set reqData='%s', respData='%s' where id=%d"%(kn.qwest, kn.answer, kn.id_)
		#print "Update ek:",unicode(req)	
		self.execQuery(unicode(req),"Error update knowlege: "+req)	
			
	def updateRepetitionKnowledge(self, kn):
		if(kn.learned == 0 and kn.newCard == 0 ):
			kn.startDate = getDate(time.time())	
		nextDate = time.time()
		nextDate += kn.interval*60*60*24
		
		req = "update facts set easyFactor=%f, interval=%d, repetition=%d, showDate=#%s#, startDate=#%s#, newCard=%d\
		where id=%d"%(kn.easyFactor, kn.interval, kn.repetition, getDate(nextDate), kn.startDate, kn.newCard, kn.id_)
		#print "Update rk:",req
		self.execQuery(unicode(req),"Error update knowlege: "+req)
	
			
	def visitEachKnowledge(self, request, consumer, errorMessage):
		try:
			self.dbv.prepare(self.db,request)
			for i in range(1,self.dbv.count_line()+1):
				self.dbv.get_line() 
				consumer(self.dbv.col)
				self.dbv.next_line()
		except SymbianError:
			self.Log(errorMessage)
			self.Log(sys.exc_info()[0])
			self.Log(sys.exc_info()[1])
			self.Log(sys.exc_info()[2])
 
	def getPracticeKnowledges(self):   
		listFacts = []	
		dateCurrent = getDate(time.time())
		showFactsReq = "select * from facts where (showDate <= #%s#) and (newCard = 0)"%(dateCurrent)
		#print u'get practice %s \n'%(showFactsReq)
		def practiceGetting(col, container=listFacts):
			kn = Knowledge(col(REQ_DATA), col(RESP_DATA))
			kn.id_ = col(ID)
			kn.easyFactor = col(EESY_FACTOR)
			kn.interval = col(INTERVAL)
			kn.repetition = col(REPETITION)
			kn.startDate = getDate(col(START_DATE))
			kn.learned = 1
			kn.newCard = col(NEW_CARD)
			container.append(kn)
			
		self.visitEachKnowledge(unicode(showFactsReq), practiceGetting ,"Error get practice fact: ")
		return listFacts
									
	def getNewKnowledges(self, maxNewKnowledges):   
		listFacts = []	
		newFactsReq = "select * from facts where newCard = 1"
		
		def newGetting(col, container=listFacts, maxKnw=maxNewKnowledges):
			if(len(container) < maxKnw):
				kn = Knowledge(col(REQ_DATA), col(RESP_DATA))
				kn.id_ = col(ID)
				kn.startDate = getDate(col(START_DATE))
				container.append(kn)
			
		self.visitEachKnowledge(unicode(newFactsReq), newGetting,"Error get new fact: ")
		return listFacts
		
	def getAllKnowledges(self):   
		listKnowledges = []	
		allFactsReq = "select * from facts"
		
		def allGetting(col, container=listKnowledges):
			kn = Knowledge(col(REQ_DATA), col(RESP_DATA))
			kn.id_ = col(ID)
			kn.easyFactor = col(EESY_FACTOR)
			kn.interval = col(INTERVAL)
			kn.repetition = col(REPETITION)
			kn.startDate = getDate(col(START_DATE))
			kn.nextDate = getDate(col(NEXT_DATE))
			kn.newCard = col(NEW_CARD)
			container.append(kn)
						
		self.visitEachKnowledge(unicode(allFactsReq), allGetting,"Error get new fact: ")
		return listKnowledges	
		
