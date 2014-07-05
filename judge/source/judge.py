#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as sql
import os, re, sys, thread, time, urllib

#mysql variables
sql_hostname = 'localhost'
sql_username = 'judge'
sql_password = 'judge'
sql_database = 'onlinejudge'


#global variables
extension_supported={"C":"c","C++":"cpp","Java":"java"}
ioeredirect  = " 0<input.txt 1>output.txt 2>error.txt"
running = 0
mypid = int(os.getpid())
timediff = 0
compiled = 0


#connection
db = sql.connect(sql_hostname,sql_username,sql_password,sql_database)
cursor = db.cursor()
#version of the DB
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s" %data
#create a table submission
cursor.execute("DROP TABLE IF EXISTS submission")
createtable_submission = """CREATE TABLE submission (problemcode char(20) NOT NULL, user char(20) NOT NULL, src_path char(100), done INT, result INT )"""
cursor.execute(createtable_submission)
#create table problems
cursor.execute("DROP TABLE IF EXISTS problems")
createtable_problems = """CREATE TABLE problems (problemcode char(20) NOT NULL, testcases_path char(100), correctoutput_path char(100))"""
cursor.execute(createtable_problems)
db.close()




def compilation_engine(code_name, lang):
	print "\nStage 1 : Compilation Started ..."
	if lang == "C" :
		os.system("gcc "+code_name+".c -lm -lcrypt -O2 -pipe -w -o "+code_name+ioeredirect)
		if not os.path.exists(code_name):
			print "\nError : Compilation error (gcc) !"
			return 0
	elif lang == "C++" :
		os.system("g++ "+code_name+".cpp -lm -lcrypt -O2 -pipe -o "+code_name+ioeredirect)
		if not os.path.exists(code_name):
			print "\nError : Compilation error (g++) !"
			return 0
	else : 
		os.system("javac "+code_name+".java"+ioeredirect);
		if not os.path.exists(code_name+".class"):
			print "\nError : Compilation error (javac) !"
			return 0
	print "Stage 1 : Compilation completed."
	global compiled 
	compiled = 1
	


def execution_engine(code_name, lang):
	
	if compiled == 0 :
		print "\nStage 2 : Not compiled terminated ..."
		return 0;
	print "\nStage 2 : Execution started ..."
	global timediff,running
	starttime = time.time()
	running = 1
	if   lang == "C"    :  os.system("./"+code_name+ioeredirect)
	elif lang == "C++"  :  os.system("./"+code_name+ioeredirect)
	elif lang == "Java" : os.system("java "+code_name+".class"+ioeredirect)
	running = 100
	endtime = time.time()
	timediff = endtime-starttime
	print "\n Success : Thread completed ! "
	print	"completed in : " 
	print timediff

def kill(code_name,lang):
	global mypid
	if lang=="C": process = code_name
	elif lang=="C++": process = code_name
	elif lang=="Java": process = "java"
	for process in os.popen("ps -A | grep "+str(process)).read().split("\n"):
		pdata = process.split();
		if(len(pdata)>0): pid = int(pdata[0])
		else: pid = -1
		if pid==mypid or pid==-1: continue
		os.system("kill -9 "+str(pid))




#-----------------testing------------------

#compilation_engine("helloworld","C")
#execution_engine("helloworld","C")

timelimit = 3
code_name = "helloworld"
lang      = "C"

print "\nStarted a new thread ..."
compilation_engine(code_name,lang)
thread.start_new_thread(execution_engine,(code_name,lang))
killtimer = time.time()
print "Sleep ..."
time.sleep(0.5)

if running != 100 :
	killtimer = float(time.time()) - float(killtimer)
	if killtimer > timelimit :
		print "Error : Time Limit Exceeded "
		print "KILL THREAD : ACTIVATED"
		kill(code_name,lang)
#---------------------------------------------




