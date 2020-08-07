#!/bin/env python3

import http, os, sys, argparse, json
from http import server
import SourceServerDriver, Drivers, BaseSystemDriver, MinecraftServerDriver

parser = argparse.ArgumentParser(description='Simple server monitoring script')
parser.add_argument('--port', type=str, dest='port', default='6500', help='Sets the port of the web server')
parser.add_argument('--dump-drivers', action='store_true', dest='dump_drivers', help='Dumps a list of all drivers')
parser.add_argument('--verbose', action='store_true', dest='verbose', help='Enables verbose logging for debugging')
parser.add_argument('drivers', metavar='D', type=str, nargs='+', help='Drivers to enable')

def get_enabled_drivers() -> list:
	enabled = []
	for drv in Drivers.drivers:
		if drv.name in sys.argv:
			enabled.append(drv)
	return enabled

def collect_data(json: dict):
	drivers = get_enabled_drivers()
	for drv in drivers:
		if not drv.should_run():
			continue
		drv.collect(json)

def do_init_pass(settings: dict):
	drivers = get_enabled_drivers()
	for drv in drivers:
		drv.init(settings)

def do_discover_pass():
	drivers = get_enabled_drivers()
	for drv in drivers:
		drv.discover_devices()

class RequestHandler(server.BaseHTTPRequestHandler):
	def do_GET(self):
		output = dict()
		collect_data(output)
		outs = json.dumps(output, indent=4)
		self.protocol_version = "HTTP/1.1"
		self.send_response(200)
		self.send_header("Content-Length", len(outs))
		self.end_headers()
		self.wfile.write(bytes(outs, "utf8"))

	def do_POST(self):
		self.send_response(404)

class ServerMonitor():
	def run(self, args):
		server_address = ('', int(args.port))
		print('Server running on locahost:{0}'.format(args.port))
		self.httpd = server.HTTPServer(server_address, RequestHandler)
		self.httpd.serve_forever()

def main():
	args = parser.parse_args()

	if args.dump_drivers:
		for i in Drivers.drivers:
			print('{0}:\t{1}'.format(i.name, i.desc))
		exit(0)

	do_init_pass({})
	do_discover_pass()
	server = ServerMonitor()
	server.run(args)

if __name__ == "__main__":
	main()