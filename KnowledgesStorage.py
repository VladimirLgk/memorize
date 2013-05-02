import e32
import e32db
import codecs
import appuifw
import key_codes
import zlib
import time
import sys

def SimpleLogger(str):
	print str
		
def getDate(timeValue):
		dateTime = e32db.format_time(timeValue).split()			   
		return dateTime[0]
		
class KnowledgeStorage:
	def __init__(self, path, Logger=None):
		if Logger == None:
			self.Log = SimpleLogger
		#self.dbPath = u'e:\\memorise\\facts.db'
		self.dbPath = path
		self.db = e32db.Dbms()
		self.dbv = e32db.Db_view()
		try:
			self.db.open(self.dbPath)
			print "the memorise data base open"
		except:
			print "the memorise data base not found create new"
			self.db.create(self.dbPath)
			self.db.open(self.dbPath)
			print "open created db and create new table"
			self.initNewStorage()
	
	def execQuery(query, errorMessage=None)
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
		execQuery(req,"Error create table:")
		
	def insertOneKnowledge(self, request, responce, sound_name):
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
		print 'result query: ', unicode(showFactsReq)

			#TODO: prepare lambda consumer
			fc = fact(self.dbv.col(2), self.dbv.col(4))
			fc.id_ = self.dbv.col(1)
			fc.easyFactor = self.dbv.col(6)
			fc.interval = self.dbv.col(7)
			fc.repetition = self.dbv.col(8)
			fc.startDate = getDate(self.dbv.col(9))
			fc.learned = 1
			listFacts.append(fc)
		
		
		visitEachKnowledge(unicode(showFactsReq), ... ,"Error get practice fact: ")
		return listFacts
									
	def getNewKnowledges(self, maxNewKnowledges):   
		listFacts = []	
		newFactsReq = "select * from facts where newCard = 1"
		
			#TODO: prepare lambda consumer
			fc = fact(self.dbv.col(2), self.dbv.col(4))
			fc.id_ = self.dbv.col(1)
			fc.newCard = 1
			fc.easyFactor = 2.5
			fc.startDate = getDate(self.dbv.col(9))
			listFacts.append(fc)
			
		visitEachKnowledge(unicode(showFactsReq), ... ,"Error get new fact: ")
		return listFacts
		
	def updateOneKnowledge(self, fact):
		if(fact.learned == 0 and fact.newCard == 0 ):
			fact.startDate = getDate(time.time())	
		nextDate = time.time()
		nextDate += fact.interval*60*60*24
		
		req = "update facts set easyFactor=%f, interval=%d, repetition=%d, showDate=#%s#, startDate=#%s#, newCard=%d\
		where id=%d"%(fact.easyFactor, fact.interval, fact.repetition, getDate(nextDate), fact.startDate, fact.newCard, fact.id_)
		execQuery(unicode(req),"Error store knowlege: "+sql_req)
		
