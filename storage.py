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

def SimpleLogger(str):
	print str
		
def getDate(timeValue):
		dateTime = e32db.format_time(timeValue).split()			   
		return dateTime[0]
		
class KnowledgeStorage:
		
	def __init__(self, path, Logger=SimpleLogger):
		self.Log = Logger
		self.db = e32db.Dbms()
		self.dbv = e32db.Db_view()
		self.open(path)
		
	def open(self, path):
		self.dbPath = path
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
		
	def	setKnowledge(self, kn, stat):
		#TODO: implement correct import
		self.insertFullNewKnowledge(kn):
	
	def insertFillNewKnowledge(self, kn):
												
		req = "insert into facts (reqData, reqSound, respData, respSound, easyFactor, interval, repetition, startDate, showDate, newCard)\
							values ('%s',%d,'%s',%d, %f, %d, %d, #%s#, #%s#, %d)" %\ 
							(kn.qwest, 0, kn.answer, 0, kn.easyFactor, kn.interval, kn.repetition, kn.startDate, kn.showDate, kn.newCard)							
		execQuery(unicode(req),"Error insert fact:")		
			
	def insertNewKnowledge(self, request, responce):
		bdate = getDate(0)													
		req = "insert into facts (reqData, reqSound, respData, respSound, easyFactor, interval, repetition, startDate, showDate, newCard)\
							values ('%s',%d,'%s',%d, %f, %d, %d, #%s#, #%s#, %d)" % (request, 0, responce, 0, 2.5, 0, 0, bdate, bdate, 1)							
		execQuery(unicode(req),"Error insert fact:")							

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
		
		def practiceGetting(col, container=listFacts):
			kn = Knowledge(col(REQ_DATA), col(RESP_DATA))
			kn.id_ = col(ID)
			kn.easyFactor = col(EESY_FACTOR)
			kn.interval = col(INTERVAL)
			kn.repetition = col(REPETITION)
			kn.startDate = getDate(col(START_DATE))
			kn.learned = 1
			container.append(kn)
			
		self.visitEachKnowledge(unicode(showFactsReq), practiceGetting ,"Error get practice fact: ")
		return listFacts
									
	def getNewKnowledges(self, maxNewKnowledges):   
		listFacts = []	
		newFactsReq = "select * from facts where newCard = 1"
		
		def newGetting(col, container=listFacts, maxKnw=maxNewKnowledges):
			if(len(listFacts) < maxKnw):
				kn = Knowledge(col(REQ_DATA), col(RESP_DATA))
				kn.id_ = col(ID)
				kn.newCard = 1
				kn.easyFactor = 2.5
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
		
	def updateOneKnowledge(self, kn):
		if(kn.learned == 0 and kn.newCard == 0 ):
			kn.startDate = getDate(time.time())	
		nextDate = time.time()
		nextDate += kn.interval*60*60*24
		
		req = "update facts set easyFactor=%f, interval=%d, repetition=%d, showDate=#%s#, startDate=#%s#, newCard=%d\
		where id=%d"%(kn.easyFactor, kn.interval, kn.repetition, getDate(nextDate), kn.startDate, kn.newCard, kn.id_)
		execQuery(unicode(req),"Error store knowlege: "+sql_req)
