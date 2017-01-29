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


dirServer = 'http://localhost:5030/dirServer'
lockServerURL = 'http://localhost:5050/lockServer'

def upload_File(filenameToSend):

	url = dirServer+"/upload"
	cwd = os.getcwd()		#current dir
	f = cwd + os.path.sep + "UserStorage" + os.path.sep + filenameToSend	
	hashvalue = hashlib.md5(open(f,'rb').read()).hexdigest()
	print("x = %s" %hashvalue)
	fileToSend={	'file' : (filenameToSend, open(f, 'rb' ))	}
	f2 = cwd + os.path.sep + "UserStorage" + os.path.sep + filenameToSend	
	fileToSend2={	'file' : (filenameToSend, open(f2, 'rb' ))	}
	dataToSend={	'fileName' : filenameToSend	,'hashvalue' : hashvalue}
	fileName={	'fileName' : filenameToSend}
	print("file to send = ")
	print(fileToSend)
	lockServerResponse= requests.get(lockServerURL+'/read',data=fileName)	
	#Get url locations to send
	#serverResponse= requests.post(url,data=dataToSend)
	lockStatus= lockServerResponse.content
	lockStatus = lockStatus.decode('utf-8')
	print("Lock status is equal to " + lockStatus)
	if(lockStatus == 'OPEN'):
		#file is open, can write to it
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
		requests.post(lockServerURL+'/unlock',data=fileName)	
		print("File is unlocked")
	else:
		print("File to write to is currently locked. Please try again later")


def readFile(filenameToRead):
	file_Server = findFileServer(filenameToRead)
	if(file_Server != None):
		url = file_Server + "/read"
		print("URL =" + url)
		fileToGet={	'file' : filenameToRead}
		if(getCacheHash(filenameToRead) != findHashValue(filenameToRead)):
			print("Local file not up to date, loading from file server")
			serverResponse= requests.get(url, json=fileToGet)
			if(serverResponse.status_code==400):
				print("Error, file not found in fileServer")

			else:
				cwd = os.getcwd()	
				fileRecieved = open(cwd+"\\" + filenameToRead,'wb')
				fileRecieved.write(serverResponse.content)
				fileRecieved.close()
				#Update Cache
				f = cwd + os.path.sep + "UserStorage" + os.path.sep + filenameToRead	
				path = cwd + os.path.sep + "Cache" + os.path.sep + filenameToRead	
				shutil.copyfile(f, path)
				print("Response = ")
				print(serverResponse)
		else:
			print("Cached file is up to date")

	else:
		print("File not found")


def getCacheHash(filenameToFind):
	try: 
		path = os.getcwd() + os.path.sep + "Cache" + os.path.sep + filenameToFind
		print("path = " + path)
		hashvalue = hashlib.md5(open(path,'rb').read()).hexdigest()
		print("hashvalue in cache = " + hashvalue)
		return hashvalue
	except:
		print("Could not find hash in cache")
		return 0

def findFileServer(filenameToFind):
	url = dirServer + "/read"
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


def findHashValue(filenameToCheck):
	url = dirServer+"/returnHash"
	cwd = os.getcwd()		#current dir
	f = cwd + os.path.sep + "Cache" + os.path.sep + filenameToCheck	
	hashvalue = hashlib.md5(open(f,'rb').read()).hexdigest()
	dataToSend={	'fileName' : filenameToCheck	,'hashvalue' : hashvalue}
	serverResponse= requests.get(url, data=dataToSend)

	if(serverResponse.status_code==400):
		print("Error, file not found on directory server")
		return None
	else:
		content=serverResponse.content
		hashvalue = content.decode('utf-8')
		print("Hash value in file server = " + hashvalue)
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

