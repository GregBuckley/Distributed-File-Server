from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
import os
import json
import shutil
import hashlib
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
		f = cwd + os.path.sep + "UserStorage" + os.path.sep + filenameToSend	
		hashvalue = hashlib.md5(open(f,'rb').read()).hexdigest()
		print("x = %s" %hashvalue)
		fileToSend={	'file' : (filenameToSend, open(f, 'rb' ))	}

		f2 = cwd + os.path.sep + "UserStorage" + os.path.sep + filenameToSend	
		fileToSend2={	'file' : (filenameToSend, open(f2, 'rb' ))	}
		
		dataToSend={	'fileName' : filenameToSend	,'hashvalue' : hashvalue}
		print("file to send = ")
		print(fileToSend)
		#Get url locations to send
		serverResponse= requests.post(url,data=dataToSend)
		content= json.loads((serverResponse.content).decode())
		masterurl = content['Master']
		repurl = content['Replicate']
		print(masterurl)
		print(repurl)

		#Save in Cache
		path = cwd + os.path.sep + "Cache" + os.path.sep + filenameToSend	
		shutil.copyfile(f, path)


		#Send files
		try:
			serverResponse= requests.post(masterurl+"/upload",files = fileToSend,data=dataToSend)
			serverResponse= requests.post(repurl+"/upload",files = fileToSend2,data=dataToSend)
		except:    # This is the correct syntax
			print ("Could NOT connect!")

		print (serverResponse)


def readFile(filenameToRead):
	fileServer = findFileServer(filenameToRead)
	if(fileServer != None):
		url = fileServer + "/read"
		print("URL =" + url)
		fileToGet={	'file' : filenameToRead}
		serverResponse= requests.get(url, json=fileToGet)
		if(serverResponse.status_code==400):
			print("Error, file not found in fileServer")

		else:
			cwd = os.getcwd()	
			fileRecieved = open(cwd+"\\" + filenameToRead,'wb')
			fileRecieved.write(serverResponse.content)
			fileRecieved.close()
			print("Response = ")
			print(serverResponse)
	else:
		print("File not found")




def findFileServer(filenameToFind):
	url = fileServers[1] + "/read"
	fileToGet={	'file' : filenameToFind}
	serverResponse= requests.get(url, json=fileToGet)
	if(serverResponse.status_code==400):
		print("Error, file not found on directory server")
		return None
	else:
		print("The file is stored here")
		content=serverResponse.content
		serverId = content.decode('utf-8')
		print(serverId)
		return serverId

def hashValid(filenameToCheck):
	url = fileServers[1]+"/returnHash"
	cwd = os.getcwd()		#current dir
	f = cwd + os.path.sep + "Cache" + os.path.sep + filenameToSend	
	hashvalue = hashlib.md5(open(f,'rb').read()).hexdigest()
	dataToSend={	'fileName' : filenameToSend	,'hashvalue' : hashvalue}
	serverResponse= requests.get(url, data=dataToSend)

	if(serverResponse.status_code==400):
		print("Error, file not found on directory server")
		return None
	else:
		print("The file is stored here")
		content=serverResponse.content
		hashvalue = content.decode('utf-8')
		print(hashvalue)
		return hashvalue

	





if __name__ == '__main__':
	while 1:
		command = input("Please enter command: 1=upload 2= read\n")
		commandArray = command.split(" ")
		if(command[0] == "1"):
			upload_File(commandArray[1])
		if(command[0] == "2"):
			readFile(commandArray[1])

	clientApp.run(host = 'localhost', port=5000, debug = True)



