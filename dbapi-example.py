def prepareMediaFile(filename)
	mdir = import_path + u'mp3\\'+ filename
    adlres = adler32(mdir)  
	newname = media_path + "%d" % (avers) + ".wav"
	print "file: ",mdir, "hash: ", adlres, "new name: ", newname
	file_copy(newname,mdir)
	os.remove(mdir)
	return adlres
	
lof = []
currFacts = 0
Stage=0
   
def quit():
  app_lock.signal()

def next_stage(): 
   global Stage
   global lof
   global currFacts
   if Stage == 0:
      appuifw.query(lof[currFacts].qwest,"query")
      Stage += 1
   elif Stage == 1:
      appuifw.query(unicode(lof[currFacts].answer),"query")
      Stage += 1
      currFacts += 1
      if currFacts >= len(lof):
         currFacts = 0
      Stage=0
   elif Stage == 2:
      Stage = 0

if __name__ == "__main__":
   global lof       
   db = memdb()
   if db.dbIsEmpty():
      print "try import file"
	  
      countImported = importFile(db, import_path+'test_card.csv')
      if  countImported > 0:
         db.removeEmptyMark()
         
   appuifw.app.title = u"Memorise"  
   appuifw.app.screen = 'large'   
   appuifw.app.exit_key_handler = quit 
   t = appuifw.Text()
   
   #t.set_pos((100,100))
   t.style = appuifw.STYLE_BOLD
   t.add(u"Try learn words")
   
   lof = db.getPracticeFacts()
   currFacts = 0
   
   appuifw.app.body.bind(key_codes.EKeySelect, next_stage)
   
   app_lock = e32.Ao_lock()  
   app_lock.wait()
	
