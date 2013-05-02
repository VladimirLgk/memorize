import e32
import appuifw
import sysinfo
import codecs
from graphics import *
from key_codes import *
			
def tabs_proc(id):
	print id

def quit():
	app_lock.signal()	
	
	

if __name__ == "__main__":
	
	appuifw.app.title = u"Memorize"  
	appuifw.app.screen = 'full'   
	appuifw.app.exit_key_handler = quit 
	
	tbs = [u'start',u'study',u'cfg']
	appuifw.app.set_tabs(tbs, changeTab)
	appuifw.app.activate_tab(0)
	app0()
	app_lock = e32.Ao_lock()  
	app_lock.wait()

