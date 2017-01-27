from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import send_file
import os
filesArray =[]
DIRECTORY = "SERVER_ONE_FOLDER"
fileServerOne = Flask(__name__)

#Function which takes a file as input and stores the file
@fileServerOne.route('/serverOne/upload', methods = ['POST'])
def recieve_File():
	if not request.files:
		return make_response(jsonify({"ERROR" : "NOT FOUND"}), 405)
	cd = get_cd()
	print ("CD = " + cd) 
	f = request.files['file']
	print(f)
	nameOfFile = request.form['fileName']
	print ("CD = " + cd+ "\\" + DIRECTORY) 
	f.save(cd+ os.path.sep + DIRECTORY + os.path.sep + nameOfFile)
	return ('file uploaded successfully', 201)



@fileServerOne.route('/serverOne/read', methods = ['GET'])
def read_File():
	print("ststststs")
	responseDictionary = request.json
	filenameToGet= responseDictionary['file']
	print("Looking for file:")
	print(filenameToGet)
	cd = get_cd()		#current dir
	f = cd +os.path.sep  + DIRECTORY + os.path.sep + filenameToGet	
	print(f)
	try:
		fileToGet= open(f,'rb')		
		return (send_file(f),200)
	except:
		abort (400)



def get_cd():
	res = os.getcwd()
	print("res = " + res)
	return res

if __name__ == '__main__':
	cwd = os.getcwd()
	if not os.path.isdir(cwd + "\\" + DIRECTORY):
		os.mkdir(cwd + "\\" + DIRECTORY)
	fileServerOne.run(host = 'localhost', port=5010, debug = True)


