import e32
import appuifw
from key_codes import *
import sysinfo
from graphics import *


class Label:
	CENTER_ALIGN = 1
	TR_ALIGN = 2
	width = 1
	aflag = CENTER_ALIGN
	visible = 0
	
	def __init__(self,text_, pos_, size_, container=None):	
		self.text = text_
		self.pos = pos_
		self.size = size_
		if(container != None):
			container.append(self)
		
	def area(self, pos_, siz_):
		self.pos = pos_
		self.size = siz_
	
	def font(self, ftype, fsize):
		self.fntSize = fsize
		self.fntType = ftype 
	
	def text(self, text_, align_):
		self.text = text_
		self.aflag = align_

	def apperance(self, outline_, fill_, width_):	
		self.outline = outline_
		self.fill = fill_
		self.width = width_
			
	def draw(self, img_):
		if (self.visible != 0):
			text_pos = (self.pos[0]+5,self.pos[1]+18)
			img_.text(text_pos, self.text)#, font=(self.fntType,self.fntSize)
		
class Button(Label):
	active = 0
	
	def hotKey(self, hotkey_):	
		self.hotkey = hotkey_
		
	def draw(self, img_):
		if(self.visible != 0):
			width_ = self.width
			if(self.active):
				width_+=2
			img_.rectangle((self.pos[0],self.pos[1], self.pos[0]+self.size[0], self.pos[1]+self.size[1]),fill=self.fill, width=width_, outline=self.outline)
			Label.draw(self, img_)
