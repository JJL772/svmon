# Driver for Source Engine servers
import ServerMonitor as svmon

class MinecraftServerDriver(svmon.BaseDriver):
	def __init__(self):
		super().__init__('MinecraftServer', 'Driver for Minecraft server monitoring')

	def init(self, settings: dict) -> bool:
		self.settings = settings 

	def discover_devices(self):
		pass

	def collect(self, json: dict) -> bool:
		return True 

	def should_run(self) -> bool:
		return True 
