import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import cmu_course_api

#Semester must be one of S (spring), M1 (Summer 1), M2 (Summer 2), or F (Fall).
semester = 'S'
# CMU AndrewID
username = 'bryanyan'
# Password 
password = '*********'
# Python Dictionary 
# data = cmu_course_api.get_course_data(semester, username, password)

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r'/', IndexHandler)]
		settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
						static_path=os.path.join(os.path.dirname(__file__), "static"),
						debug=True)
		tornado.web.Application.__init__(self, handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class MCSHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('mcs.html')

class SCSHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('scs.html')

class DCHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('dc.html')

class CITHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('cit.html')

class CFAHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('cfa.html')

class TPHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('tepper.html')

if __name__ == '__main__':
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()