from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
from flask import send_file
from OpenSSL import SSL
import os
DIRECTORY = "SERVER_X_FOLDER"
fileServerX = Flask(__name__)

serverPort ='0'
context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), os.getcwd()+os.path.sep+'HTTPS CERTS'+os.path.sep+'FS1'+os.path.sep+'server.crt')
key = os.path.join(os.path.dirname(__file__), os.getcwd()+os.path.sep+'HTTPS CERTS'+os.path.sep+'FS1'+os.path.sep+'server.key')
DIR_SERVER = 'https://localhost:5030/dirServer'

#Function which takes a file as input and stores the file
@fileServerX.route('/upload', methods = ['POST'])
def recieve_File():
	if not request.files:
		return make_response(jsonify({"ERROR" : "NOT FOUND"}), 405)
	cd = get_cd()
	print ("CD = " + cd) 
	f = request.files['file']
	print(f)
	nameOfFile = request.form['fileName']
	print ("CD = " + cd+ "\\" + serverPort) 
	f.save(cd+ os.path.sep + serverPort +"_Folder"+ os.path.sep + nameOfFile)
	return ('file uploaded successfully', 200)

#Returns the bytes of a file requested if stored in file server.
@fileServerX.route('/read', methods = ['GET'])
def read_File():
	responseDictionary = request.json
	filenameToGet= responseDictionary['file']
	print("Looking for file:")
	print(filenameToGet)
	cd = get_cd()		#current dir
	f = cd+ os.path.sep + serverPort +"_Folder"+ os.path.sep + filenameToGet
	print(f)
	try:
		fileToGet= open(f,'rb')		
		return (send_file(f),200)
	except:
		abort (400)




#Returns the current working directory.
def get_cd():
	res = os.getcwd()
	print("res = " + res)
	return res

if __name__ == '__main__':
	serverPort = input("\nPlease enter port to run fileServer. (Reccommended Ports: 5060 - 5090):\n")

	cwd = os.getcwd()
	if not os.path.isdir(cwd + "\\" + serverPort+"_Folder"):
		os.mkdir(cwd + "\\" + serverPort+"_Folder")

	serverURL =  {'serverURL': 'https://localhost:'+serverPort}
	serverResponse= requests.post(DIR_SERVER+"/addServer",data=serverURL, verify = False)
	context = (cer,key)
	fileServerX.run(host = 'localhost', port=serverPort, debug = False,ssl_context=context)


