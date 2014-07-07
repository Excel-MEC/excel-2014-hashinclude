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


# stage 1 compilation. 
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


# stage 2 execution.	
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
	print "\nThread completed ! "
	print "Stage 2 : execution completed in : " 
	print timediff


#force killing of a thread after Timelimit for the problem.
def kill(code_name,lang):
	print "Time Limit Exceeded"
	print "Force : Killing the thread !"
	global mypid
	if lang=="C": process = code_name
	elif lang=="C++": process = code_name
	elif lang=="Java": process = "java"
	for process in os.popen("ps -A | grep "+str(process)).read().split("\n"):
		pdata = process.split();
		print pdata
		if(len(pdata)>0): pid = int(pdata[0])
		else: pid = -1
		if pid==mypid or pid==-1: continue
		os.system("kill -9 "+str(pid))




#-----------------testing------------------

timelimit = 1
code_name = "helloworld"
lang      = "C++"

compilation_engine(code_name,lang)
thread.start_new_thread(execution_engine,(code_name,lang))
#killtimer = time.time()
time.sleep(timelimit) #IF the program doesnot finish the force kill the thread.
kill(code_name,lang)


#---------------------------------------------




