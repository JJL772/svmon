import time, datetime

def error(str: str):
	print('\u001b[91m',end='')
	print('[{1}] ERROR: {0}'.format(str, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	print('\u001b[39m', end='')
	
def warning(str: str):
	print('\u001b[93m',end='')
	print('[{1}] WARN: {0}'.format(str, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	print('\u001b[39m', end='')

def info(str: str):
	print('[{1}] {0}'.format(str, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


class BaseDriver():

	def __init__(self, name, desc = ""):
		self.name = name
		self.desc = desc 

	"""
	Initializes the driver and any data we have in it
	"""
	def init(self, settings: dict) -> bool:
		pass 

	"""
	Discovers "devices" 
	"""
	def discover_devices(self):
		pass 

	"""
	Returns if the driver should run or not
	"""
	def should_run(self) -> bool:
		raise NotImplementedError()

	"""
	Collects data from devices into the dictionary
	"""
	def collect(self, json: dict) -> bool:
		raise NotImplementedError()
