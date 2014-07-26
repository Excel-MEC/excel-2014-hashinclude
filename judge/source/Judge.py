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
cleaned  = 0

#clean out all system level calls in c 
def cleaner(code_name, lang):
	print "\nStage 0 : Cleaning "
	global cleaned	
	cleaned = 0
	if lang == "C":
		filename = code_name+".c"
		#filter out dangerous functions and headers
		dangers_c = ['system(','fork(','<CON','execl(','wait(','exit(','<signal.h>','<fcntl.h>','socket.h']
		lines = [line.strip() for line in open(filename)]
		#remove all white spaces from each line and then filter out the danger
		for line in lines:
			line = re.sub(r'\s+', '', line)
			for danger in dangers_c:
				if danger in line:
					print "Error : Potential threat detected !"
					print "Line  : "+line
					cleaned +=1 ;
	else:
		print "Error : unidentified lang"
		cleaned = 1


# stage 1 compilation. 
def compilation_engine(code_name, lang):
	if cleaned:
		print "\nStage 1 : stopping need to clean the code !"
		return 0

	print "\nStage 1 : Compilation Started ..."
	if lang == "C" :
		os.system("gcc "+code_name+".c -lm -lcrypt -O2 -pipe -w -o "+code_name+ioeredirect)
		if not os.path.exists(code_name):
			print "Error : Compilation error (gcc) !"
	elif lang == "C++" :
		os.system("g++ "+code_name+".cpp -lm -lcrypt -O2 -pipe -o "+code_name+ioeredirect)
		if not os.path.exists(code_name):
			print "Error : Compilation error (g++) !"
	else : 
		os.system("javac "+code_name+".java"+ioeredirect);
		if not os.path.exists(code_name+".class"):
			print "Error : Compilation error (javac) !"
			
	print "Stage 1 : Compilation completed."
	global compiled 
	compiled = 1


# stage 2 execution.	
def execution_engine(code_name, lang):
	if compiled == 0 :
		print "\nStage 2 : Not compiled terminated ..."
		return 0

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
	print "Thread completed ! "
	print "Stage 2 : execution completed in : " 
	print timediff


#force killing of a thread after Timelimit for the problem.
def kill(code_name,lang):
	print "\nStage 3 : Time Limit Exceeded --> Killing the thread"
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
lang      = "C"

cleaner(code_name,lang)
compilation_engine(code_name,lang)
thread.start_new_thread(execution_engine,(code_name,lang))
#killtimer = time.time()
time.sleep(timelimit) #IF the program doesnot finish the force kill the thread.
kill(code_name,lang)


#---------------------------------------------