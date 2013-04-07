import e32
import e32db
import codecs
import appuifw
import key_codes
import zlib

class fact:      
   def __init__(self, qwest, answer):
      self.qwest = qwest
      self.answer = answer
      self.remeber = 0

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
      self.db.execute(u'create table symple_facts (id counter, avers_know varchar(128),sound_hash0 bigint, revers_know varchar(128), sound_hash1 bigint)')
      self.db.execute(u"insert into symple_facts (avers_know, sound_hash0,revers_know, sound_hash1 ) values ('empty',55,'full',55)")
      print "finished create table"
   
   def insertKnowns(self, avers, revers, sound_name):
      sql_req = "insert into symple_facts (avers_know, sound_hash0, revers_know, sound_hash1) values ('%s',%d,'%s',%d)" % (avers, 0, revers, 0)
      print 'result query: ', unicode(sql_req)
      self.db.execute(unicode(sql_req))
      print "insert knowns in table"   
      
   
   def getPracticeFacts(self):   
      listFacts = []
      self.dbv.prepare(self.db,u"select * from symple_facts")
      for i in range(1,self.dbv.count_line()+1):
         self.dbv.get_line() 
         fc = fact(self.dbv.col(2), self.dbv.col(4))
         listFacts.append(fc)
         self.dbv.next_line()
      return listFacts   
  
	  

