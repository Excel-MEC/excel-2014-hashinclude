#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as sql
import os, re, sys, threading, time, urllib
from mainapp.models import Submission
import filecmp

class solution_verificationThread(threading.Thread):
    def __init__(self, threadID, name, counter,submissionid, problemid,folder_name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.submissionid = submissionid
        self.problemid = problemid
        self.foldername = folder_name
    def run(self):
        print "Starting " + self.name
        solution_verification(self.submissionid,self.problemid,self.foldername)
        print "Exiting " + self.name

class killThread (threading.Thread):
    def __init__(self, threadID, name, counter,code_name, lang, submissionid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.code_name = code_name
        self.lang = lang
        self.submissionid = submissionid
    def run(self):
        print "Starting " + self.name
        kill(self.code_name,self.lang,self.submissionid)
        print "Exiting " + self.name

class execThread (threading.Thread):
    def __init__(self, threadID, name, counter,code_name, lang, submissionid, problemid,folder_name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.code_name = code_name
        self.lang = lang
        self.submissionid = submissionid
        self.problemid = problemid
        self.foldername = folder_name
    def run(self):
        print "Starting " + self.name
        execution_engine(self.code_name, self.lang, 1,self.submissionid,self.problemid,self.foldername)
        print "Exiting " + self.name

#connection
'''db = sql.connect(sql_hostname,sql_username,sql_password,sql_database)
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
db.close()'''

def ioe_redirect_create(submissionid='',foldername='',problemid=''):
    ioeredirect  = " 0<mainapp/media/question_"+str(problemid)+"/testcases.txt 1>mainapp/media"+str(foldername)+"/output-"+str(submissionid)+".txt 2>mainapp/media"+str(foldername)+"/error-"+str(submissionid)+".txt"
    print ioeredirect
    return ioeredirect

#clean out all system level calls in c 
def cleaner(code_name, lang):
    print "\nStage 0 : Cleaning "
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


# stage 1 compilation. 
def compilation_engine(code_name, lang, submissionid,problemid,foldername):
    ioeredirect=ioe_redirect_create(submissionid,foldername,problemid)
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
    return 1

# stage 2 execution.    
def execution_engine(code_name, lang, compiled,submissionid,problemid,foldername):
    if compiled == 0 :
        print "\nStage 2 : Not compiled terminated ..."
        return 0
    print "\nStage 2 : Execution started ..."
    ioeredirect=ioe_redirect_create(submissionid,foldername,problemid)
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
    c = Submission.objects.get(id=submissionid)
    c.status = "Executed Successfully"
    c.save()
    thread3 = solution_verificationThread(3, "Thread-SolVerification", 3,str(submissionid), str(problemid),str(foldername))
    thread3.start()
    print timediff


#force killing of a thread after Timelimit for the problem.
def kill(code_name,lang,submissionid=0):
    timelimit=1
    time.sleep(timelimit) #IF the program doesnot finish the force kill the thread.
    print "Time Limit Exceeded"
    print "Force : Killing the thread !"
    mypid = int(os.getpid())
    if lang=="C": process = code_name
    elif lang=="C++": process = code_name
    elif lang=="Java": process = "java"
    loop = os.popen("ps -A | grep "+str(process)).read().split("\n")
    print loop
    for process in loop:
        pdata = process.split();
        print pdata
        if(len(pdata)>0): pid = int(pdata[0])
        else: pid = -1
        if pid==mypid or pid==-1: continue
        os.system("kill -9 "+str(pid))
        c = Submission.objects.get(id=submissionid)
        c.status = "Timeout"
        c.save()

def solution_verification(submissionid, problemid,foldername):
    solutionpath = "mainapp/media/question_"+problemid+"/output.txt"
    playeroutputpath = "mainapp/media"+foldername+"/output-"+submissionid+".txt"
    S = Submission.objects.get(id=submissionid)
    print solutionpath
    print playeroutputpath
    if filecmp.cmp(solutionpath, playeroutputpath):
        S.status = "Success"
    else:
        S.status = "Failed testcases"
    S.save()

#-----------------testing------------------

'''timelimit = 1
code_name = "test"
lang      = "C++"

compilation_engine(code_name,lang)

thread1 = killThread(1, "Thread-kill", 1,code_name,lang,0)
thread2 = execThread(2, "Thread-exec", 2,code_name,lang,0)

thread1.start()
thread2.start()

print "Exiting main program"'''
#---------------------------------------------




