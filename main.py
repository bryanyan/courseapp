import os.path
import io
import json
from pprint import pprint

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
					(r'/scs', SCSHandler),
					(r'/([0-9][0-9][0-9][0-9][0-9])', FCEHandler)]
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

	def get(self):
		courses = self.getSCSCourses()
		self.render('scs.html', courses=courses)

class FCEHandler(tornado.web.RequestHandler):

	def getFCEs(self):
		fces = {}
		for i in xrange(1, len(fce)):
			courseID = str(fce[i]["Course ID"])
			year = fce[i]["Year"]
			if year < 2011: continue
			if courseID == "": continue
			elif "FA14-" in courseID:
				courseID = courseID.strip("FA14")
				courseID = courseID.strip("-")
			elif "F13-" in courseID: 
				courseID = courseID.strip("F13")
				courseID = courseID.strip("-")
			if courseID in fces:
				fces[courseID].append(fce[i])
			else:
				fces[courseID] = []
		return fces


	def parseFCEs(self, course):
		fces = self.getFCEs()

		calculated = {"Hours Per Week": 0, "Feedback to Students": 0, "Explains Subject Matter": 0, "Overall Teaching": 0, 
					  "Overall Course": 0, "Responses": 0, "count": 0}

		courseFCEs = fces[course]

		for i in xrange(len(courseFCEs)):
			#calculated["Hours Per Week"] += courseFCEs[i]["Questions"]['1: Hrs Per Week 9']
			calculated["Feedback to Students"] += courseFCEs[i]["Questions"]["5: Feedback to students"]
			calculated["Explains Subject Matter"] += courseFCEs[i]["Questions"]["7: Explains subject matter"]
			calculated["Overall Teaching"] += courseFCEs[i]["Questions"]["9: Overall teaching"]
			calculated["Overall Course"] += courseFCEs[i]["Questions"]["10: Overall course"]
			calculated["Responses"] += courseFCEs[i]["Responses"]
			calculated["count"] += 1

		numInputs = calculated["count"]
		calculated["Feedback to Students"] = int(round(((float(calculated["Feedback to Students"])/numInputs)/5)*100))
		calculated["Explains Subject Matter"] = int(round(((float(calculated["Explains Subject Matter"])/numInputs)/5)*100))
		calculated["Overall Teaching"] = int(round(((float(calculated["Overall Teaching"])/numInputs)/5)*100))
		calculated["Overall Course"] = int(round(((float(calculated["Overall Course"])/numInputs)/5)*100))

		return calculated


	def get(self, course):
		fces = self.parseFCEs(course)
		self.write(fces)

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