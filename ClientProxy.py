from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
import os
import json
filesArray =[]

clientApp = Flask(__name__)
#fileServers = {1 : 'http://localhost:5010/serverOne',
#				2 : 'http://localhost:5020/serverTwo'}

fileServers = {1 : 'http://localhost:5030/dirServer'}

def upload_File(filenameToSend):
	for fileServerID in fileServers:
		url = fileServers[fileServerID]
		url = url+"/upload"
		cwd = os.getcwd()		#current dir
		f = cwd + "\\" + filenameToSend	
		fileToSend={	'file' : (filenameToSend, open(f, 'rb' ))	}
		print (fileToSend)
		print (filenameToSend)
		dataToSend={	'fileName' : filenameToSend	}
		serverResponse= requests.post(url,files = fileToSend,data=dataToSend)
		print (serverResponse)


def read_File(filenameToRead):
	url = fileServers[1] + "/read"
	fileToGet={	'file' : filenameToRead}
	serverResponse= requests.get(url, json=fileToGet)
	print("The file is stored here")
	d=serverResponse.content
	print(d)
	





if __name__ == '__main__':
	while 1:
		command = input("Please enter command: 1=upload 2= read\n")
		commandArray = command.split(" ")
		if(command[0] == "1"):
			upload_File(commandArray[1])
		if(command[0] == "2"):
			read_File(commandArray[1])

	clientApp.run(host = 'localhost', port=5000, debug = True)



