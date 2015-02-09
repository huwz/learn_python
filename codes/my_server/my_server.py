# -*- coding= utf-8 -*-

################################################
#
#  author: 		huwz
#
#  date:		Mon, 09, Feb 2015 00:20:10
#
################################################

from BaseHTTPServer import *

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		# url : 127.0.0.1:2000/search?name=huwz&pwd=123456

		# version_string() return server version
		print 'server version:		%s'%self.version_string()			# 'BaseHTTP/0.3 Python/2.7.2'

		# sys_version
		print 'sys version:		%s'%self.sys_version 					# 'Python/2.7.2'

		# error_message_format
		print 'format:'
		print self.error_message_format

		# <head>
		# <title>Error response</title>
		# </head>
		# <body>
		# <h1>Error response</h1>
		# <p>Error code %(code)d.
		# <p>Message: %(message)s.
		# <p>Error code explanation: %(code)s = %(explain)s.
		# </body>

		# BaseHTTPRequestHandler.path
		print 'path:			%s'%self.path 							# 'search?name=huwz&pwd=123456'

		# client_address
		# ('127.0.0.1', 61421)
		print 'client address: 	%s:%d'%(self.client_address[0], self.client_address[1])

		# address_string: client hostname
		print 'client hostname:	%s'%self.address_string()				# 'huwz.mapbar.com'

		# command
		print 'request method:		%s'%self.command					# 'GET'

		# log_data_time_string()
		print 'time:			%s'%self.log_date_time_string()			# '09/Feb/2015 10:22:37'

		# data_time_string()
		print 'timestamp:		%s'%self.date_time_string()				# 'Mon, 09 Feb 2015 02:28:20 GMT'

		# request_verison
		print 'request version:	%s'%self.request_version 				# 'HTTP/1.1'

		# send_response()
		self.send_response(200, 'ok')       							# log_message('%s - - [%s] "%s %s %s" %d -', self.address_string, self.log_data_time_string(), self.command, self.path, self.request_version, 200)
																		# 'huwz.mapbar.com - - [09/Feb/2015 10:34:44] "GET /search?%20name=huwz&pwd=123456 HTTP/1.1" 200 -'

		# log_request()
		self.log_request(301, 100)										# log_message('%s - - [%s] "%s %s %s" %d %d', self.address_string, self.log_data_time_string(), self.command, self.path, self.request_version, 301, 100)
																		# 'huwz.mapbar.com - - [09/Feb/2015 10:34:44] "GET /search?%20name=huwz&pwd=123456 HTTP/1.1" 301 100'

		# log_error()
		self.log_error('log_error():%s', 'no error')					# log_message('%s - - [%s] %s', self.address_string, self.log_data_time_string(), 'log_error():no error')
																		# 'huwz.mapbar.com - - [09/Feb/2015 10:34:44] log_error():no error'

	def do_POST():
		pass

def main():
	server = HTTPServer(('', 2000), MyHandler)
	server.serve_forever()

if __name__ == '__main__':
	main()