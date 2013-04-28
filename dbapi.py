import e32
import e32db
import codecs
import appuifw
import key_codes
import zlib
import time
import sys

class fact:      
	def __init__(self, qwest_, answer_):
		self.id_ = 0
		self.qwest = qwest_
		self.answer = answer_
		self.repetition = 0
		self.easyFactor = 0
		self.interval = 0
		self.showDate = 0
		self.learned = 0
		self.newCard = 0
		self.startDate = ""
		
def getDate(timeValue):
		dateTime = e32db.format_time(timeValue).split()			   
		return dateTime[0]
		
class memdb:
	def __init__(self):
		self.dbPath = u'e:\\memorise\\facts.db'
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
			self.createTables()
				   
	
				   
	def createTables(self):
		#create new table for knowledged
		try:
			self.db.execute(u'create table facts (id counter, reqData varchar(128),reqSound bigint,respData varchar(128),\
			respSound bigint, easyFactor float, interval integer,repetition integer, startDate date, showDate date, newCard integer)')
		except SymbianError:
			print "Error create table: "
			print sys.exc_info()[0]
			print sys.exc_info()[1]
			print sys.exc_info()[2]	
		#self.insertKnowns('unknown','unknown', 0)
		print "finished create table"

	def insertKnowns(self, request, responce, sound_name):
		bdate = getDate(0)
														
		sql_req = "insert into facts (reqData, reqSound, respData, respSound, easyFactor, interval, repetition, startDate, showDate, newCard)\
							values ('%s',%d,'%s',%d, %f, %d, %d, #%s#, #%s#, %d)" % (request, 0, responce, 0, 2.5, 0, 0, bdate, bdate, 1)
		try:
			self.db.execute(unicode(sql_req))
			print "insert knowns in table"  
		except SymbianError:
			print "Error insert fact: "
			print sys.exc_info()[0]
			print sys.exc_info()[1]
			print sys.exc_info()[2] 
                                                                                                                                                                                                                   
   
	def getPracticeFacts(self):   
		dateCurrent = getDate(time.time())
		showFactsReq = "select * from facts where (showDate <= #%s#) and (newCard = 0)"%(dateCurrent)
		print 'result query: ', unicode(showFactsReq)
		
		try:
			self.dbv.prepare(self.db,unicode(showFactsReq))
		except SymbianError:
			print "Error get practice fact: "
			print sys.exc_info()[0]
			print sys.exc_info()[1]
			print sys.exc_info()[2] 
			return []
			
		listFacts = []	
		for i in range(1,self.dbv.count_line()+1):
			self.dbv.get_line() 
			fc = fact(self.dbv.col(2), self.dbv.col(4))
			fc.id_ = self.dbv.col(1)
			fc.easyFactor = self.dbv.col(6)
			fc.interval = self.dbv.col(7)
			fc.repetition = self.dbv.col(8)
			fc.startDate = self.dbv.col(9)
			fc.learned = 1
			listFacts.append(fc)
			self.dbv.next_line()
		return listFacts	
									
	def getNewFacts(self, maxNewCard):   
		newFactsReq = "select * from facts where newCard = 1"
		
		try:
			self.dbv.prepare(self.db,unicode(newFactsReq))
		except SymbianError:
			print "Error get new fact: "
			print sys.exc_info()[0]
			print sys.exc_info()[1]
			print sys.exc_info()[2] 
			return []
		
		requestsCard = self.dbv.count_line()
		if maxNewCard < requestsCard:
			requestsCard = maxNewCard
		listFacts = []	
		for i in range(1,requestsCard+1):
			self.dbv.get_line() 
			fc = fact(self.dbv.col(2), self.dbv.col(4))
			fc.id_ = self.dbv.col(1)
			fc.newCard = 1
			fc.easyFactor = 2.5
			fc.startDate = getDate(self.dbv.col(9))
			listFacts.append(fc)
			self.dbv.next_line()
		return listFacts
		
	def storeFact(self, fact):
		if(fact.learned == 0 and fact.newCard == 0 ):
			fact.startDate = getDate(time.time())	
		nextDate = time.time()
		nextDate += fact.interval*60*60*24
		sql_req = "update facts set easyFactor=%f, interval=%d, repetition=%d, showDate=#%s#, startDate=#%s#, newCard=%d\
		where id=%d"%(fact.easyFactor, fact.interval, fact.repetition, getDate(nextDate), fact.startDate, fact.newCard, fact.id_)
							
		try:
			print "try to store:",sql_req	
			self.db.execute(unicode(sql_req))
		except SymbianError:
			print "Error store fact: "
			print sys.exc_info()[0]
			print sys.exc_info()[1]
			print sys.exc_info()[2]
		
