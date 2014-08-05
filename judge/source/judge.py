#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as sql
import os, re, sys, threading, time, urllib
from mainapp.models import Submission
import filecmp
from multiprocessing import Process

class solution_verificationThread(threading.Thread):
    def __init__(self, threadID, name, counter,submissionid, problemid,folder_name):
        super(solution_verificationThread, self).__init__()
        self._stop = threading.Event()
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
    def stop(self):
        self._stop.set()


class killThread (threading.Thread):
    def __init__(self, threadID, name, counter,code_name, lang, submissionid,problemid,foldername):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.code_name = code_name
        self.lang = lang
        self.submissionid = submissionid
        self.problemid = problemid
        self.foldername = foldername
    def run(self):
        print "Starting " + self.name
        kill(self.code_name,self.lang,self.submissionid,self.problemid,self.foldername)
        print "Exiting " + self.name


class execThread (threading.Thread):
    def __init__(self, threadID, name, counter,code_name, lang, submissionid, problemid,folder_name):
        super(execThread, self).__init__()
        self._stop = threading.Event()
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
    def stop(self):
        self._stop.set()

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

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
def ioe_redirect_create(submissionid='',foldername='',problemid=''):
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ioeredirect  = " 0<"+str(BASE_PATH)+"/mainapp/media/question_"+str(problemid)+"/testcases.txt 1>"+str(BASE_PATH)+"/mainapp/media"+str(foldername)+"/output-"+str(submissionid)+".txt 2>"+str(BASE_PATH)+"/mainapp/media"+str(foldername)+"/error-"+str(submissionid)+".txt"
    print ioeredirect
    return ioeredirect

#clean out all system level calls in c 
def cleaner(code_name, lang):
    print "\nStage 0 : Cleaning "
    if lang == "C" or lang == "C++":
        if lang == "C":
            filename = code_name+".c"
        else:
            filename = code_name+".cpp"
            
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
    print "./ "+code_name+ioeredirect
    if   lang == "C"    :  os.system(code_name+ioeredirect)
    elif lang == "C++"  :  os.system(code_name+ioeredirect)
    elif lang == "Java" : os.system("java "+code_name+".class"+ioeredirect)
    running = 100
    endtime = time.time()
    timediff = endtime-starttime
    print "\nThread completed ! "
    print "Stage 2 : execution completed in : " 
    os.system("rm "+code_name)
    print timediff
    return 0


#force killing of a thread after Timelimit for the problem.
def kill(code_name,lang,submissionid,problemid,foldername):
    timelimit=1
    c = Submission.objects.get(id=submissionid)
    p = Process(target=execution_engine, args=(code_name, lang, 1,submissionid,problemid,foldername,))
    p.start()
    time.sleep(timelimit) #IF the program doesnot finish the force kill the thread.
    if not p.is_alive():
        p.join()
    print os.popen("ps -A | grep "+str(p.pid)).read().split("\n")
    
    try:
        os.kill(p.pid, 0)
        c = Submission.objects.get(id=submissionid)
        c.status = "Timeout"
        c.save()
        time.sleep(0.5)
        os.system("kill -9 "+str(p.pid))
        print "Force killed Execution"
        return True
    except OSError:
        thread3 = solution_verificationThread(3, "Thread-SolVerification", 3,str(submissionid), str(problemid),str(foldername))
        thread3.start()
        return False

def solution_verification(submissionid, problemid,foldername):
    solutionpath = str(BASE_PATH)+"/mainapp/media/question_"+problemid+"/output.txt"
    playeroutputpath = str(BASE_PATH)+"/mainapp/media"+foldername+"/output-"+submissionid+".txt"
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



