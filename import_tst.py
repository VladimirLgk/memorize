import e32
import e32db
import codecs
import appuifw
import key_codes
import zlib
import audio
import os
import math

import_path = u'e:\\memorise\\import\\'
media_path = u'e:\\memorise\\media\\'

listoffile = []

def prepareMediaFile(filename):
	mdir = unicode(import_path + u'mp3\\'+ filename)
	adlres = abs(zlib.adler32(mdir))  
	newname = unicode(media_path + "%x" % (adlres) + ".wav")
	print "file: ",mdir, "hash: ", adlres, "new name: ", newname
	if not os.access(newname,os.F_OK):
		e32.file_copy(newname,mdir)
		#os.remove(mdir)
	listoffile.append(newname)
	return adlres
	  
def importFile(filename):
	f = codecs.open(filename, "r", "cp1251")
	listOfWords = f.readlines()
	counter = 0
	for x in listOfWords:
		knowns = x.split('\t',4)
		ps = 0
		filehash0 = 0
		filehash1 = 0
		for k in knowns:
			if(ps == 0):
				print "request: ", knowns[0]
			elif(ps == 1):	
				print "answer: ", knowns[1]
			elif(ps == 2):
				if len(knowns[2]) > 5:
					print "sound0: ", knowns[2]
					filehash0 = prepareMediaFile(knowns[2])
					print "sounds0 hash: ", filehash0
			elif(ps == 3):	
				if  len(knowns[3]) > 5:
					print "sound1: ", knowns[3]
					filehash1 = prepareMediaFile(knowns[3])
					print "sounds1 hash: ", filehash1			
			ps +=1
		counter += 1	
		#db.insertKnowns(knowns[0], knowns[1],filehash0, filehash1)
	print "read strings: ", counter
	return counter;
   
  
pos = 0   

def playing():
    global S
    try:
		#print "try playing: " , listoffile[pos]
		S = audio.Sound.open(listoffile[pos])
		S.play(1,0,NextItem)
    except:
        print "Record first a sound!"

def closing():
    global S
    S.stop()
    S.close()
    #print "Stopped"		

def NextItem( prev, current, error):
	global pos
	if current == audio.EOpen and prev == audio.EPlaying:
		closing()
		pos += 1
		#print "new position: " , pos
		if pos < len(listoffile):
			playing()
		

def quit():
  app_lock.signal()   		
	   
if __name__ == "__main__":
	
	appuifw.app.exit_key_handler = quit 
	
	countImported = importFile( import_path+'test_card.csv')
	if len(listoffile) > 0:
		print "Run play all....", len(listoffile)
		playing()
	else:
		print "No composition for play...."
	
	app_lock = e32.Ao_lock()  
	app_lock.wait()		