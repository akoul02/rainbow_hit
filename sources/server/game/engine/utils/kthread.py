import threader
import threading
from time import sleep

# this code was copy-pasted from here: 
# https://github.com/munawarb/Python-Kill-Thread-Extension

class KThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.stopped = False # This is the flag we'll use to signal thread termination.

	def is_alive(self):
		return not self.stopped

	def end(self):
		if self.is_alive():
			threader.killThread(self.ident)
			self.stopped = True