# Driver for Source Engine servers
import ServerMonitor as svmon
import psutil, os, sys, platform

class BaseSystemDriver(svmon.BaseDriver):
	def __init__(self):
		super().__init__('BaseSystem', 'Driver for base system monitoring')

	def init(self, settings: dict) -> bool:
		self.settings = settings 

	def discover_devices(self):
		pass

	def collect(self, json: dict) -> bool:
		sys_info = {}
		sys_info["operating_system"] = platform.system()
		sys_info["processor"] = platform.processor()
		sys_info["arch"] = platform.uname().machine
		sys_info["node"] = platform.uname().node
		sys_info["os_ver"] = platform.release()
		sys_info["num_cpus"] = int(psutil.cpu_count())
		sys_info["cpu_usage_total"] = float(psutil.cpu_percent())
		meminfo = psutil.virtual_memory()
		sys_info["mem_total"] = meminfo.total 
		sys_info["mem_used"] = meminfo.used
		sys_info["mem_free"] = meminfo.free 
		swapinfo = psutil.swap_memory()
		sys_info["swap_free"] = swapinfo.free
		sys_info["swap_used"] = swapinfo.used
		sys_info["swap_total"] = swapinfo.total
		sys_info["cpu_info"] = []
		cpu_freqs = psutil.cpu_freq(percpu=True)
		cpu_usages = psutil.cpu_percent(percpu=True)
		cpu_temps = psutil.sensors_temperatures()
		for i in range(psutil.cpu_count()):
			cpuinfo = {}
			cpuinfo["freq"] = float(cpu_freqs[i][0])
			cpuinfo["usage"] = float(cpu_usages[i])
			try:
				cpuinfo['temp'] = float(cpu_temps['coretemp'][i].current)
			except:
				pass
			sys_info["cpu_info"].append(cpuinfo)

		netinfo = psutil.net_io_counters()
		sys_info["net_info"] = {
			"bytes_sent": netinfo.bytes_sent,
			"bytes_recv": netinfo.bytes_recv,
			"packets_sent": netinfo.packets_sent,
			"packets_recv": netinfo.packets_recv
		}
		sys_info["fs_info"] = {
			"root": {
				"used": psutil.disk_usage('/').used,
				"free": psutil.disk_usage('/').free,
				"total": psutil.disk_usage('/').total,
				"percent": psutil.disk_usage('/').percent
			},
			"nfs": {
				"used": psutil.disk_usage('/nfs/').used,
				"free": psutil.disk_usage('/nfs/').free,
				"total": psutil.disk_usage('/nfs/').total,
				"percent": psutil.disk_usage('/nfs/').percent
			}
		}
		sys_info["num_processes"] = len(psutil.pids())
		json["system_info"] = sys_info
		return True 

	def should_run(self) -> bool:
		return True 
