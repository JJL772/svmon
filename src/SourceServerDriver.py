# Driver for Source Engine servers
import ServerMonitor as svmon
import json, os, platform, psutil, datetime

class SourceServer():
	def __init__(self):
		self.pid = 0
		self.running = False
		self.memory_percent = 0.0
		self.memory_used = 0
		self.memory_virtual = 0
		self.cpu_usage = 0.0
		self.handles = 0
		self.thread_count = 0
		self.create_time = 0
		self.exe = ''
		self.pid_file = ''
		self.desc = ''
		self.name = ''

	def clear(self):
		self.memory_percent = self.memory_used = self.memory_virtual = 0
		self.cpu_usage = 0
		self.thread_count = 0
		self.create_time = 0
		self.running = False

	def to_dict(self) -> dict:
		ret = {}
		ret['pid'] = self.pid
		ret['running'] = self.running
		ret['memory_percent'] = self.memory_percent
		ret['memory_used'] = self.memory_used
		ret['memory_virtual'] = self.memory_virtual
		ret['cpu_usage'] = self.cpu_usage
		ret['handles'] = self.handles
		ret['thread_count'] = self.thread_count
		ret['create_time'] = self.create_time
		ret['exe'] = self.exe
		ret['pid_file'] = self.pid_file
		ret['desc'] = self.desc
		ret['name'] = self.name
		ret['create_time_nice'] = datetime.datetime.fromtimestamp(self.create_time).strftime('%Y-%m-%d %H:%M:%S')
		return ret 
		

class SourceServerDriver(svmon.BaseDriver):
	def __init__(self):
		super().__init__('SourceEngineServer', 'Driver for Source Engine servers')
		self.servers = []
		self.discovered = False

	def init(self, settings: dict) -> bool:
		self.settings = settings 
		# Read /etc/svmon/source_servers.json
		self.settings_json = dict()
		with open('/etc/svmon/source_servers.json', 'r') as fp:
			self.settings_json = json.load(fp)
		return True

	def discover_devices(self):
		if self.settings_json is None or self.discovered == True:
			return
		self.discovered = True
		try:
			for server in self.settings_json:
				srv = SourceServer()
				srv.pid_file = server['pid_file']
				srv.name = server['name']
				srv.desc = server['desc']
				self.servers.append(srv)
		except:
			svmon.error('Malformed config: /etc/svmon/source_servers.json')
			raise

	def collect(self, json: dict) -> bool:
		server_info = []
		try:
			for server in self.servers:
				server.running = False
				server.clear()
				try:
					if not os.path.exists(server.pid_file):
						svmon.warning('server pidfile does not exist" {0}'.format(server.pid_file))
						continue
					# Try to read the PID from the pid file
					with open(server.pid_file, 'r') as fp:
						server.pid = int(fp.readline())
					# try to open the PID
					proc = psutil.Process(pid=server.pid)
					procinfo = proc.as_dict()
					server.clear()
					server.exe = procinfo['exe']
					server.running = True
					server.create_time += procinfo['create_time']
					# Read each child process (and the parent process lol)
					for child in proc.children(recursive=True) + [proc]:
						procinfo = child.as_dict()
						server.cpu_usage += procinfo['cpu_percent']
						server.thread_count += procinfo['num_threads']
						server.memory_percent += procinfo['memory_percent']
						server.memory_used += procinfo['memory_full_info'].uss
						server.memory_virtual += procinfo['memory_info'].vms
				except:
					pass
				server_info.append(server.to_dict())
		except:
			return False
		json['source_servers'] = server_info
		return True 

	def should_run(self) -> bool:
		# only run if the config actually exists 
		return os.path.exists('/etc/svmon/source_servers.json') 
