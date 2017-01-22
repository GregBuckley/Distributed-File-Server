from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import g
import sqlite3
import os
filesArray =[]
DIRECTORY = "\DIRECTORY_Server\\"
fileServerOne = Flask(__name__)

fileServers = {1 : 'http://localhost:5010/serverOne',
				2 : 'http://localhost:5020/serverTwo'}

#Recieve File
#Check if file has been sent before
#Update Pre existing file or write as new
#Put into all available file servers and update Database
@fileServerOne.route('/dirServer/upload', methods = ['POST'])
def recieve_File():
	if not request.files:
		return make_response(jsonify({"ERROR" : "NOT FOUND"}), 404)
	cd = get_cd()
	print ("CD = " + cd) 
	f = request.files['file']
	nameOfFile = request.form['fileName']
	data = request.form['fileName']
	print ("CD = " + cd+ "\\" + DIRECTORY) 
	f.save(cd+ "\\" + DIRECTORY + nameOfFile)
	upload_File(nameOfFile)
	return ('file uploaded successfully', 201)

#Upload file into all available databases as a new file or update previous
#If pre existing, mark "not up to date" on database for fileservers who are not up to date
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



def get_cd():
	res = os.getcwd()
	return res

if __name__ == '__main__':
	cwd = os.getcwd()
	if not os.path.isdir(cwd + "\\" + DIRECTORY):
		os.mkdir(cwd + "\\" + DIRECTORY)
	fileServerOne.run(host = 'localhost', port=5020, debug = True)


