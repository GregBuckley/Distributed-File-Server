from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from OpenSSL import SSL
import requests
import os
import json
import shutil
import hashlib

clientApp = Flask(__name__)
DIR_SERVER = 'https://localhost:5030/dirServer'
LOCK_SERVER = 'https://localhost:5050/lockServer'
USER_STORAGE = os.getcwd() + os.path.sep + "UserStorage" + os.path.sep
CACHE = os.getcwd() + os.path.sep + "Cache" + os.path.sep 

#declare security certificates
context = SSL.Context(SSL.SSLv23_METHOD)
cert = os.path.join(os.path.dirname(__file__), os.getcwd()+os.path.sep+'HTTPS certTS'+os.path.sep+'Client'+os.path.sep+'server.crt')
key = os.path.join(os.path.dirname(__file__), os.getcwd()+os.path.sep+'HTTPS certTS'+os.path.sep+'Client'+os.path.sep+'server.key')


def upload_File(filenameToSend):

	url = DIR_SERVER+"/upload"
	cwd = os.getcwd()		#current dir
	f = USER_STORAGE + filenameToSend
	try:
		hashvalue = hashlib.md5(open(f,'rb').read()).hexdigest()
		fileToSend={	'file' : (filenameToSend, open(f, 'rb' ))	}
		f2 = USER_STORAGE + filenameToSend	
		fileToSend2={	'file' : (filenameToSend, open(f2, 'rb' ))	}
		dataToSend={	'fileName' : filenameToSend	,'hashvalue' : hashvalue}
		fileName={	'fileName' : filenameToSend}
		print(filenameToSend + " successfully found in user storage.")
		lockServerResponse= requests.get(LOCK_SERVER+'/read',data=fileName, verify = False)	
		#Get url locations to send
		lockStatus= lockServerResponse.content
		lockStatus = lockStatus.decode('utf-8')
		print("Lock status on file is " + lockStatus)
		if(lockStatus == 'OPEN'):
			#file is open, can write to it
			serverResponse= requests.post(url,data=dataToSend,verify = False)
			content= json.loads((serverResponse.content).decode())
			masterurl = content['Master']
			print("MasterURL ===== " + masterurl)
			repurl = content['Replicate']
			#Save in Cache
			path = CACHE + filenameToSend	
			shutil.copyfile(f, path)
			#Send files
			try:
				serverResponse= requests.post(masterurl+"/upload",files = fileToSend,data=dataToSend, verify = False)
				serverResponse= requests.post(repurl+"/upload",files = fileToSend2,data=dataToSend, verify = False)
				print("Successfully written to file")
			except:    # This is the correct syntax
				print ("Could not connect to file servers")

			#Files sent, release lock on files.
			requests.post(LOCK_SERVER+'/unlock',data=fileName, verify = False)	
			print("Lock on file released")
		else:
			print("File to write to is currently locked. Please try again later")
	except:
		print("File not found in User Storage")


def readFile(filenameToRead):
	file_Server = findFileServer(filenameToRead)
	cwd = os.getcwd()	
	if(file_Server != None):
		url = file_Server + "/read"
		print("URL =" + url)
		fileToGet={	'file' : filenameToRead}
		#Check if current cached file is up to date. If so, load from it; otherwise load from file Server and update cache.
		if(getCacheHash(filenameToRead) != findHashValue(filenameToRead)):
			print("Local file not up to date, loading from file server")
			serverResponse= requests.get(url, json=fileToGet, verify = False)
			if(serverResponse.status_code==400):
				print("Error, file not found in fileServer")

			else:
				fileRecieved = open(USER_STORAGE+ filenameToRead,'wb')
				fileRecieved.write(serverResponse.content)
				fileRecieved.close()
				#Update Cache
				f = USER_STORAGE + filenameToRead	
				path = CACHE+ filenameToRead	
				shutil.copyfile(f, path)
		else:
			print("Cached file is up to date. Loading file in from cache.")
			f = USER_STORAGE+filenameToRead	
			path = CACHE + filenameToRead	
			shutil.copyfile(path,f)

	else:
		print("File not found")

#Function which finds the hash value of the file located in the cache.
def getCacheHash(filenameToFind):
	try: 
		path = CACHE + filenameToFind
		hashvalue = hashlib.md5(open(path,'rb').read()).hexdigest()
		return hashvalue
	except:
		print("Could not find hash in cache")
		return 0

#Calls the dir server and requests the url of the file server where the file is located.
def findFileServer(filenameToFind):
	url = DIR_SERVER + "/read"
	fileToGet={	'file' : filenameToFind}
	serverResponse= requests.get(url, json=fileToGet, verify = False)
	if(serverResponse.status_code==400):
		print("Error, file not found on directory server")
		return None
	else:
		print("FileServer containing file found.")
		content=serverResponse.content
		serverId = content.decode('utf-8')
		return serverId

#Calls the dir server and requests the hash value of the file in the file server which is being sought.
def findHashValue(filenameToCheck):
	url = DIR_SERVER+"/returnHash"
	cwd = os.getcwd()
	f = CACHE + filenameToCheck	
	hashvalue = hashlib.md5(open(f,'rb').read()).hexdigest()
	dataToSend={	'fileName' : filenameToCheck	,'hashvalue' : hashvalue}
	serverResponse= requests.get(url, data=dataToSend, verify = False)

	if(serverResponse.status_code==400):
		print("Error, file not found on directory server")
		return None
	else:
		content=serverResponse.content
		hashvalue = content.decode('utf-8')
		print("Hash value in file server = " + hashvalue)
		return hashvalue

if __name__ == '__main__':
	context = (cert,key)	#declare ssl context
	while 1:
		command = input("\nPlease enter a command using keywords 'write' and 'read' fllowed by the file you wish to act on. \nEg: 'write test.PNG'\n")
		commandArray = command.split(" ")
		#Seperate user commands by eaith calling a "write" or a "read"
		if(command[0] == "w" or command[0] == "W"  ):
			upload_File(commandArray[1])
		
		if(command[0] == "r" or command[0] == "R"):
			readFile(commandArray[1])




	clientApp.run(host = 'localhost', port=5000, debug = True, ssl_context=context)

