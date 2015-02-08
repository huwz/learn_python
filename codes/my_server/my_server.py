# -*- coding= utf-8 -*-

from BaseHTTPServer import *

################################################
#
#  author: 		huwz
#
#  date:		Mon, 09 Feb 2015 00:20:10
#
################################################

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print self.path
		self.send_response(200, 'ok')
	def do_POST():
		pass

def main():
	server = HTTPServer(('', 2000), MyHandler)
	server.serve_forever()

if __name__ == '__main__':
	main()