from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
import os
import json
filesArray =[]

clientApp = Flask(__name__)
fileServers = {1 : 'http://localhost:5010/serverOne',
				2 : 'http://localhost:5020/serverTwo'}

def upload_File(filenameToSend):
	for fileServerID in fileServers:
		url = fileServers[fileServerID]
		url = url+"/upload"
		cwd = os.getcwd()
		f = cwd + "\\" + filenameToSend
		fileToSend={
			'file' : (filenameToSend, open(f, 'rb' ))
		}
		print (fileToSend)
		print (filenameToSend)
		dataToSend={
		'fileName' : filenameToSend
		}
		serverResponse= requests.post(url,files = fileToSend,data=dataToSend)
		print (serverResponse)
        
if __name__ == '__main__':
	while 1:
		command = input("Please enter command: 1=upload")
		commandArray = command.split(" ")
		if(command[0] == "1"):
			upload_File(commandArray[1])

	clientApp.run(host = 'localhost', port=5000, debug = True)



