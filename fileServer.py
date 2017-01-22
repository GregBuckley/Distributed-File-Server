from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import os
filesArray =[]
DIRECTORY = "\SERVER_ONE_FOLDER\\"
fileServerOne = Flask(__name__)

@fileServerOne.route('/serverOne/upload', methods = ['POST'])
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
	return ('file uploaded successfully', 201)

def get_cd():
	res = os.getcwd()
	return res

if __name__ == '__main__':
	cwd = os.getcwd()
	if not os.path.isdir(cwd + "\\" + DIRECTORY):
		os.mkdir(cwd + "\\" + DIRECTORY)
	fileServerOne.run(host = 'localhost', port=5010, debug = True)


