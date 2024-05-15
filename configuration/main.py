/*{
	"CREDIT": "Mad Team",
	"DESCRIPTION": "Control Franka Robot",
	"TAGS": "data",
	"VSN": "1.0",
	"INPUTS": [
		{ "LABEL": "Setup/IP", "NAME": "ip", "TYPE": "string", "DEFAULT": "192.168.1.195"},
		{ "LABEL": "Setup/authString", "NAME": "auth_string", "TYPE": "string", "DEFAULT": "authorization=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiZnJhIiwicm9sZSI6eyJhdXRob3JpemF0aW9uIjpbeyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJUYXNrcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2tpbGxzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJQYXJhbWV0ZXJzIn0seyJwZXJtaXNzaW9uIjoiUmVhZFdyaXRlIiwicmVzb3VyY2UiOiJFeGVjdXRpb24ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlN0YXR1cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQnVuZGxlcyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiU2NyaXB0cyJ9LHsicGVybWlzc2lvbiI6IlJlYWRXcml0ZSIsInJlc291cmNlIjoiQWRtaW4ifSx7InBlcm1pc3Npb24iOiJSZWFkV3JpdGUiLCJyZXNvdXJjZSI6IlNhZmV0eSJ9XSwibmFtZSI6ImFkbWluIn19.rGp0QvF1_d96hbWbetPr4Eg7DVJ4drO8cz8bpUqONj17_LkezZSakqZ72u3gXjXaInA6OM97m-bu4thgFdgblw"},
		{ "LABEL": "Setup/xControlToken", "NAME": "control_token", "TYPE": "string", "DEFAULT": "q4ZspA4bhSlA9C9kS3Y0JYEqdnmDqIlZwcPFdE1gMJ8="},

		{ "LABEL": "Franka/Open Breaks", "NAME": "open_breaks", "TYPE": "bool", "DEFAULT": false, "FLAGS": "button"},
		{ "LABEL": "Franka/Stop", "NAME": "stop", "TYPE": "event"},

		{ "LABEL": "Tasks/Update Tasks List", "NAME": "update_tasks_list", "TYPE": "event"},
		{ "LABEL": "Tasks/Task", "NAME": "task", "TYPE": "long", "DEFAULT": "None", "VALUES": ["None"]},
		{ "LABEL": "Tasks/Play", "NAME": "play_task", "TYPE": "bool", "FLAGS": "trigger,button"},

		{ "LABEL": "Positions/Update Positions", "NAME": "update_positions", "TYPE": "event"},
		{ "LABEL": "Positions/x [m]", "NAME": "pos_x", "TYPE": "string", "DEFAULT": "", "FLAGS": "read_only"},
		{ "LABEL": "Positions/y [m]", "NAME": "pos_y", "TYPE": "string", "DEFAULT": "", "FLAGS": "read_only"},
		{ "LABEL": "Positions/z [m]", "NAME": "pos_z", "TYPE": "string", "DEFAULT": "", "FLAGS": "read_only"},
		{ "LABEL": "Positions/Joint Angles", "NAME": "positions", "TYPE": "string", "DEFAULT": "", "FLAGS": "read_only,textarea"},

		{ "LABEL": "Logs/Errors", "NAME": "errors", "TYPE": "string", "DEFAULT": "Your data have not been sent.", "FLAGS": "read_only,textarea,no_label", "DESCRIPTION": "Informations and errors from MadMapper and Open Weather API."},
	]
}*/

import os
import json

class FrankaModule:
	def init(self,event):
		mad.log("Initializing FrankaModule")

		mad.listen("/self/open_breaks", "onOpenBreaks")
		mad.listen("/self/stop", "onStop")
		mad.listen("/self/update_positions", "updatePositions")
		mad.listen("/self/update_tasks_list", "updateTasksList")
		mad.listen("/self/play_task", "playTask")


		self.httpGetPos = None
		self.httpGetTaskList = None
		self.httpPlayTask = None
		self.httpStopTask = None

		self.httpPost = mad.create("http_post")
		mad.listen(self.httpPost+"/response", "onHttpResponse")

		self.timeSinceLastRefresh = 5
		self.updateTasksList(None)

	def loop(self,event):
		self.timeSinceLastRefresh = self.timeSinceLastRefresh + event["elapsed_time"] / 1000

		if self.timeSinceLastRefresh >= 1:
			self.timeSinceLastRefresh = 0
			# mad.log("Franka Http Request")

	def updatePositions(self, event):
		if self.httpGetPos == None:
			self.httpGetPos = mad.create("http_get", {"parse_json_response": False})
			mad.listen(self.httpGetPos+"/response", "onGetPosHttpResponse")

		url = "https://" + mad.get("/self/ip") + "/desk/api/robot/configuration"
		headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": mad.get("/self/auth_string"), "X-Control-Token": mad.get("/self/control_token")}

		mad.set(self.httpGetPos + "/http_url", url)
		mad.set(self.httpGetPos + "/headers", headers)
		mad.set(self.httpGetPos + "/run", True)

	def onGetPosHttpResponse(self,event):
		response = mad.get(self.httpGetPos+"/response")
		status = mad.get(self.httpGetPos+"/http_status")

		if status == 0:
			mad.set("/self/errors", "Everything seems good.")
			jsonResponse = json.loads(response)
			jsonResponse.pop("estimatedForces")
			mad.set("/self/positions", json.dumps(jsonResponse))
			mad.set("/self/pos_x", json.dumps(jsonResponse["cartesianPose"][12]))
			mad.set("/self/pos_y", json.dumps(jsonResponse["cartesianPose"][13]))
			mad.set("/self/pos_z", json.dumps(jsonResponse["cartesianPose"][14]))
		else:
			errorMessage = response
			mad.set("/self/errors", errorMessage)

	def onOpenBreaks(self,event):
		if event["value"]:
			mad.log("Opening breaks");

			url = "https://" + mad.get("/self/ip") + "/desk/api/robot/open-brakes"
			headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": mad.get("/self/auth_string"), "X-Control-Token": mad.get("/self/control_token")}

			mad.set(self.httpPost+"/http_url", url)
			mad.set(self.httpPost+"/data", "\"force\": \"false\"")
			mad.set(self.httpPost + "/headers", headers)
			mad.set(self.httpPost+"/run", True)
		else:
			mad.log("Closing breaks");

			url = "https://" + mad.get("/self/ip") + "/desk/api/robot/close-brakes"
			headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": mad.get("/self/auth_string"), "X-Control-Token": mad.get("/self/control_token")}

			mad.set(self.httpPost+"/http_url", url)
			mad.set(self.httpPost + "/headers", headers)
			mad.set(self.httpPost+"/run", True)

	def updateTasksList(self,event):
		if self.httpGetTaskList == None:
			self.httpGetTaskList = mad.create("http_get", {"parse_json_response": False})
			mad.listen(self.httpGetTaskList+"/response", "onGetTaskListHttpResponse")

		url = "https://" + mad.get("/self/ip") + "/desk/api/timelines"
		headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": mad.get("/self/auth_string"), "X-Control-Token": mad.get("/self/control_token")}

		mad.set(self.httpGetTaskList+"/http_url", url)
		mad.set(self.httpGetTaskList + "/headers", headers)
		mad.set(self.httpGetTaskList+"/run", True)


		# response = send_get_request(url, auth=self.AUTH_TOKEN)
		# # Process the response and return the status
		# processed_response = process_response(response, log_level=self.log)
		# task_names = []
		# for i in range(len(processed_response)):
		#     task_names.append(processed_response[i]['id'])
		# print(task_names)
		# return task_names

	def onGetTaskListHttpResponse(self,event):
		response = mad.get(self.httpGetTaskList+"/response")
		status = mad.get(self.httpGetTaskList+"/http_status")

		if status == 0:
			mad.set("/self/errors", "Everything seems good.")

			jsonResponse = json.loads(response)

			taskNames = []
			for i in range(len(jsonResponse)):
				taskName = jsonResponse[i]['id']
				taskNames.append(taskName)
				mad.log(taskName)

			mad.set_attr_settings("/self/task",{"entries":taskNames})
		else:
			errorMessage = response

	def playTask(self,event):
		if event["value"]:
			if self.httpPlayTask == None:
				self.httpPlayTask = mad.create("http_post")
				mad.listen(self.httpPlayTask+"/response", "onPlayTaskHttpResponse")

			url = "https://" + mad.get("/self/ip") + "/desk/api/execution"
			headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": mad.get("/self/auth_string"), "X-Control-Token": mad.get("/self/control_token")}
			#data = "{\"id\": \"" + mad.get("/self/task") +"\"}"
			#data = json.dumps({"id": str(mad.get("/self/task"))})
			data = "id="+str(mad.get("/self/task"))
			mad.log("Initialize Play Task, url \"" + url + "\" with data " + str(data))

			mad.log("Play Task, url \"" + url + "\" with data " + str(data))

			mad.set(self.httpPlayTask+"/http_url", url)
			mad.set(self.httpPlayTask+"/headers", headers)
			mad.set(self.httpPlayTask+"/data", data)
			mad.set(self.httpPlayTask+"/run", True)

	def onPlayTaskHttpResponse(self,event):
		response = mad.get(self.httpPlayTask+"/response")
		status = mad.get(self.httpPlayTask+"/http_status")

		mad.log("Play task response: " + response)

		if status == 0:
			mad.set("/self/errors", "Everything seems good.")
		else:
			errorMessage = response
			mad.set("/self/errors", errorMessage)

	def onStop(self,event):
		if event["value"]:
			mad.log("Stopping")
			if self.httpStopTask == None:
				self.httpStopTask = mad.create("http_delete")
				mad.listen(self.httpStopTask+"/response", "onStopHttpResponse")

			url = "https://" + mad.get("/self/ip") + "/desk/api/execution"
			headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": mad.get("/self/auth_string"), "X-Control-Token": mad.get("/self/control_token")}

			data = ""
			mad.log("Stop Task, url \"" + url + "\"")

			mad.set(self.httpStopTask+"/http_url", url)
			mad.set(self.httpStopTask+"/headers", headers)
			mad.set(self.httpStopTask+"/data", data)
			mad.set(self.httpStopTask+"/run", True)

	def onStopHttpResponse(self,event):
		response = mad.get(self.httpStopTask+"/response")
		status = mad.get(self.httpStopTask+"/http_status")

		mad.log("Stop task response: " + response)

		if status == 0:
			mad.set("/self/errors", "Everything seems good.")
		else:
			errorMessage = response
			mad.set("/self/errors", errorMessage)

	def onHttpResponse(self,event):
		response = mad.get(self.httpPost+"/response")
		status = mad.get(self.httpPost+"/http_status")

		if status == 0:
			mad.set("/self/errors", "Everything seems good.")
		else:
			errorMessage = response
			mad.set("/self/errors", errorMessage)

def createInstance():
	return FrankaModule()

