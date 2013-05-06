import e32
import appuifw
import sys

sys.path.append("e:\data\python");

from ui import MemorizeUi
from processor import KnowledgeProcessor
from storage import KnowledgeStorage
from serialize import Serialize

storage_path = u'e:\\memorise\\'
import_path = u'e:\\memorise\\import\\'
media_path = u'e:\\memorise\\media\\'

def tabs_proc(id):
	print id

def quit():
	app_lock.signal()	
	
if __name__ == "__main__":
	
	storage = KnowledgeStorage(u'facts.db',storage_path)
	ser = Serialize(storage)
	proc = KnowledgeProcessor(storage)
	
	
	ui = MemorizeUi(u"Memorize", quit)
	ui.setFileCallback(ser.importFile, ser.exportFile)
	ui.setStudyCallback(proc.nextKnowledge, proc.resultKnowledgeRepetition, proc.startLearn)
	ui.setDatabaseCallback(storage.open, storage.dbName)
	ui.setEditCallback(proc.getCurrentKnowledge, proc.setCurrentKnowledge)
	ui.main.show()
	
	app_lock = e32.Ao_lock()  
	app_lock.wait()

