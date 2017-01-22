from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import g
import requests

import sqlite3
import os
filesArray =[]
DIRECTORY = "\DIRECTORY_Server\\"
dirServer = Flask(__name__)

fileServers = {1 : 'http://localhost:5010/serverOne',
				2 : 'http://localhost:5020/serverTwo'}

FILE_DATABASE = "dirserdb.db"

#Recieve File
#Check if file has been sent before
#Update Pre existing file or write as new
#Put into all available file servers and update Database
@dirServer.route('/dirServer/upload', methods = ['POST'])
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
		print("File to send = %c", filenameToSend)
		cwd = os.getcwd()		#current dir
		f = cwd + "\\" + filenameToSend	
		fileToSend={	'file' : (filenameToSend, open(f, 'rb' ))	}
		print (fileToSend)
		print (filenameToSend)
		dataToSend={	'fileName' : filenameToSend	}
		sentSuccessfully = 0
		try:
			serverResponse= requests.post(url,files = fileToSend,data=dataToSend)
			sentSuccessfully=1
		except:    # This is the correct syntax
			print ("Could NOT connect!")

		if (sentSuccessfully ==1):
			print (serverResponse)
			print ( "ADD TO LIST")
		else:
			print ("DO NOT ADD")

def createDatabase():
	if (not os.path.isfile(FILE_DATABASE)):
		print ("Create DataBase %s" % FILE_DATABASE)
		connectionMaster = sqlite3.connect(FILE_DATABASE)
		cursorMaster = connectionMaster.cursor()
		#Create columns in Data Base
		sql_command = """CREATE TABLE fileDirectory ( filename VARCHAR(30) PRIMARY KEY, master_server VARCHAR(100),replicate_server VARCHAR(100) , hashValue VARCHAR (200));"""
		cursorMaster.execute(sql_command)
		connectionMaster.commit()

		#Add first values into database
		sql_command = "INSERT INTO fileDirectory VALUES(?,?,?,?);"
		params = ("File name", "master server name", "replicate server name", "hash value of file")
		cursorMaster.execute(sql_command, params)
		connectionMaster.commit()		
	else: 
		print ("DB %s already exits:" % FILE_DATABASE)
		#print database
		printDB("fileDirectory", "dirserdb.db")


def printDB(nameOfDB, DataBase_NAME):
	connection = sqlite3.connect(DataBase_NAME)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM {}".format(nameOfDB))
	db = cursor.fetchall()
	print ("-------------------------------")
	for x in db:
		print (x)
	print ("-------------------------------")

def get_cd():
	res = os.getcwd()
	return res

if __name__ == '__main__':
	cwd = os.getcwd()
	print("START THEM UP BURBY")
	createDatabase()
	if not os.path.isdir(cwd + "\\" + DIRECTORY):
		os.mkdir(cwd + "\\" + DIRECTORY)
	dirServer.run(host = 'localhost', port=5030, debug = True)


