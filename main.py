import os.path
import io
import json
import pprint

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

def getCourses():
	with open('static/courses.json') as dataFile:
		data = json.load(dataFile)
	return data['courses']

def getFCEs():
	with open('static/courses.json') as dataFile:
		data = json.load(dataFile)
	return data['fces']

data = getCourses()
fce = getFCEs()

class Application(tornado.web.Application):

	def __init__(self):
		handlers = [(r'/', IndexHandler),
					(r'/scs', SCSHandler)]
		settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
						static_path=os.path.join(os.path.dirname(__file__), "static"),
						ui_modules={"Course": CourseModule},
						debug=True)
		tornado.web.Application.__init__(self, handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

#class MCSHandler(tornado.web.RequestHandler):
#	def get(self):
#		self.render('mcs.html')

class SCSHandler(tornado.web.RequestHandler):

	def getSCSCourses(self):
		scsCourses = {}
		for i in range(15050, 15720):
			try:
				course = data[str(i)]
				scsCourses[str(i)] = course
			except:
				continue
		scsCoursesList = scsCourses.items()
		scsCoursesSorted = sorted(scsCoursesList,key=lambda x: x[0])
		return scsCoursesSorted

	def getSCSFCEs(self):
		scsFCEs = {}
		for i in range(1, len(fce)):
			courseID = str(fce[i]["Course ID"])
			if courseID == "": continue
			elif "FA14-" in courseID:
				courseID = courseID.strip("FA14")
				courseID = courseID.strip("-")
			elif "F13-" in courseID: 
				courseID = courseID.strip("F13")
				courseID = courseID.strip("-")
			if courseID in scsFCEs:
				pass
			else:
				scsFCEs[courseID] = []
		return scsFCEs

	def get(self):
		pprint.pprint(self.getSCSFCEs())
		self.render('scs.html', courses=self.getSCSCourses())

#class DCHandler(tornado.web.RequestHandler):
#	def get(self):
#		self.render('dc.html')

#class CITHandler(tornado.web.RequestHandler):
#	def get(self):
#		self.render('cit.html')

#class CFAHandler(tornado.web.RequestHandler):
#	def get(self):
#		self.render('cfa.html')

#class TPHandler(tornado.web.RequestHandler):
#	def get(self):
#		self.render('tepper.html')

class CourseModule(tornado.web.UIModule):
	def render(self, course):
		return self.render_string("modules/courses.html", course=course)

	def embedded_css(self):
		return ".course {margin-bottom: 15px}"

if __name__ == '__main__':
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()