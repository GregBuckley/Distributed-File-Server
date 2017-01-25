from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import os
filesArray =[]
DIRECTORY = "\SERVER_TWO_FOLDER\\"
fileServerTwo = Flask(__name__)

@fileServerTwo.route('/serverTwo/upload', methods = ['POST'])
def recieve_File():
	if not request.files:
		return make_response(jsonify({"ERROR" : "NOT FOUND"}), 405)
	cd = get_cd()
	print ("CD = " + cd) 
	f = request.files['file']
	nameOfFile = request.form['fileName']
	data = request.form['fileName']
	print ("CD = " + cd+ "\\" + DIRECTORY) 
	f.save(cd+ "\\" + DIRECTORY + nameOfFile)
	return ('file uploaded successfully', 201)

@fileServerTwo.route('/serverTwo/read', methods = ['GET'])
def read_File():
	print("ststststs")
	responseDictionary = request.json
	filenameToGet= responseDictionary['file']
	print("Looking for file:")
	print(filenameToGet)
	cd = get_cd()		#current dir
	f = cd +"\\" + DIRECTORY + filenameToGet	
	print(f)
	try:
		fileToGet= open(f,'r')		
		return (send_file(f),200)
	except:
		abort(400)

def get_cd():
	res = os.getcwd()
	return res

if __name__ == '__main__':
	cwd = os.getcwd()
	if not os.path.isdir(cwd + "\\" + DIRECTORY):
		os.mkdir(cwd + "\\" + DIRECTORY)
	fileServerTwo.run(host = 'localhost', port=5020, debug = True)


