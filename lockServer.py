from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from OpenSSL import SSL
from flask import g
import requests
import copy
from random import randint


import sqlite3
import os
DIRECTORY = "\Lock_Server\\"
lockServer = Flask(__name__)


context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), os.getcwd()+os.path.sep+'HTTPS CERTS'+os.path.sep+'Locking_Server'+os.path.sep+'server.crt')
key = os.path.join(os.path.dirname(__file__), os.getcwd()+os.path.sep+'HTTPS CERTS'+os.path.sep+'Locking_Server'+os.path.sep+'server.key')


LOCK_DATABASE = "lockdb.db"


def createDatabase():
	if (not os.path.isfile(LOCK_DATABASE)):
		print ("Create DataBase %s" % LOCK_DATABASE)
		connectionMaster = sqlite3.connect(LOCK_DATABASE)
		cursorMaster = connectionMaster.cursor()
		#Create columns in Data Base
		sql_command = """CREATE TABLE lockDirectory ( filename VARCHAR(30) PRIMARY KEY, lock_status VARCHAR(100));"""
		cursorMaster.execute(sql_command)
		connectionMaster.commit()

		#Add first values into database
		sql_command = "INSERT INTO lockDirectory VALUES(?,?);"
		params = ("File name", "Lock Status")
		cursorMaster.execute(sql_command, params)
		connectionMaster.commit()		
	else: 
		print ("DB %s already exits:" % LOCK_DATABASE)
		#print database

	printDB("lockDirectory", "lockdb.db")



def printDB(nameOfDB, DataBase_NAME):
	connection = sqlite3.connect(DataBase_NAME)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM {}".format(nameOfDB))
	db = cursor.fetchall()
	print ("-------------------------------")
	for x in db:
		print (x)
	print ("-------------------------------")


@lockServer.route('/lockServer/unlock', methods = ['POST'])
def releaseLock():
	nameOfFile = request.form['fileName']
	connectionMaster = sqlite3.connect(LOCK_DATABASE)
	cursorMaster = connectionMaster.cursor()
	com = "UPDATE lockDirectory SET lock_status = ? WHERE filename = ?;"
	params = ('OPEN',nameOfFile)
	cursorMaster.execute(com,params)
	connectionMaster.commit()	
	printDB("lockDirectory", "lockdb.db")
	return ('file sucessfully unlocked', 200)

#Returns the address of the file server for the client to contact to recieve their file
@lockServer.route('/lockServer/read', methods = ['GET'])
def check_If_Lock_Open():
	printDB("lockDirectory", "lockdb.db")

	filenameToGet = request.form['fileName']
	connectionMaster = sqlite3.connect(LOCK_DATABASE)
	cursorMaster = connectionMaster.cursor()
	cursorMaster.execute("SELECT lock_status FROM lockDirectory WHERE filename = ?;", (filenameToGet,))
	lock_status = cursorMaster.fetchall()
	print("lock_status is equal to = ")
	print(lock_status)
	#First time file in DB. Add and set to "Locked"
	if (not lock_status):
		print("Adding New File to Lock Database")
		cursorMaster = connectionMaster.cursor()
		sql_command = "INSERT INTO lockDirectory VALUES(?,?);"
		params = (filenameToGet, "LOCKED")
		cursorMaster.execute(sql_command, params)
		connectionMaster.commit()	
		printDB("lockDirectory", "lockdb.db")
		lock_status = "OPEN"
		return (lock_status), 200

	else:
		#lock_status = lock_status([0][0])
		com = "UPDATE lockDirectory SET lock_status = ? WHERE filename = ?;"
		params = ('LOCKED',filenameToGet)
		cursorMaster.execute(com,params)
		connectionMaster.commit()	
		printDB("lockDirectory", "lockdb.db")
		return (lock_status[0][0]), 200







if __name__ == '__main__':
	context = (cer,key)
	cwd = os.getcwd()
	createDatabase()
	#check_If_Lock_Open()
	if not os.path.isdir(cwd + "\\" + DIRECTORY):
		os.mkdir(cwd + "\\" + DIRECTORY)
	lockServer.run(host = 'localhost', port=5050, debug = False, ssl_context=context)

