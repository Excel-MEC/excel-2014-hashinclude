import os, re, sys, threading, time, urllib
from mainapp.models import Submission, Problem, Player
import filecmp
from multiprocessing import Process
import subprocess
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class solution_verificationThread(threading.Thread):
    def __init__(self, threadID, name, counter,submissionid, problemid,folder_name,userid):
        super(solution_verificationThread, self).__init__()
        self._stop = threading.Event()
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.submissionid = submissionid
        self.problemid = problemid
        self.foldername = folder_name
        self.userid = userid
    def run(self):
        print "Starting " + self.name
        solution_verification(self.submissionid,self.problemid,self.foldername,self.userid)
        print "Exiting " + self.name
    def stop(self):
        self._stop.set()


class killThread (threading.Thread):
    def __init__(self, threadID, name, counter,code_name, lang, submissionid,problemid,foldername,userid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.code_name = code_name
        self.lang = lang
        self.submissionid = submissionid
        self.problemid = problemid
        self.foldername = foldername
        self.userid = userid
    def run(self):
        print "Starting " + self.name
        kill(self.code_name,self.lang,self.submissionid,self.problemid,self.foldername,self.userid)
        print "Exiting " + self.name


class SandboxExec (object):
    def __init__(self, cmd,ioe):
        self.cmd = cmd
        self.input = open(ioe[0][2:],'r')
        self.output = open(ioe[1][2:],'w')
        self.error = open(ioe[2][2:],'w')
        print self.error
        self.process = None

    def run(self, timeout,submissionid):
        def target():
            print 'Thread started'
            env = dict(os.environ)
            env['LD_PRELOAD'] = BASE_PATH+'/EasySandbox/EasySandbox.so'
            self.process = subprocess.Popen(self.cmd, stdin=self.input, stdout=self.output, stderr=self.error, env=env)
            self.process.communicate()
            print 'Thread finished'

        thread = threading.Thread(target=target)
        starttime = time.time()
        thread.start()
        thread.join(timeout)
        endtime = time.time()
        c = Submission.objects.get(id=submissionid)
        c.status = "Failed Testcases"
        if thread.is_alive():
            c.status = "Timeout"
            print 'Terminating process'
            self.process.terminate()
            endtime = time.time()
            thread.join()
        timediff = endtime - starttime
        c.timetaken = timediff
        c.save()
    
def ioe_redirect_create(submissionid='',foldername='',problemid=''):
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ioeredirect  = " 0<"+str(BASE_PATH)+"/mainapp/media/question_"+str(problemid)+"/testcases.txt 1>"+str(BASE_PATH)+"/mainapp/media"+str(foldername)+"/output-"+str(submissionid)+".txt 2>"+str(BASE_PATH)+"/mainapp/media"+str(foldername)+"/error-"+str(submissionid)+".txt"
    return ioeredirect

#clean out all system level calls in c 
def cleaner(code_name, lang, submissionid):
    S = Submission.objects.get(id=submissionid)
    print "\nStage 0 : Cleaning "
    if lang == "C" or lang == "C++":
        if lang == "C":
            filename = code_name+".c"
        else:
            filename = code_name+".cpp"
        #filter out dangerous functions and headers
        dangers = []
        #dangers = ['system(','fork(','<CON','execl(','execlp(','wait(','<signal.h>','<fcntl.h>','socket.h','unistd.h','<csignal>','<thread>','pthread.h','syscall','CreateProcess','ShellExecute','sys/','netinet/in.h','netdb.h','kill(']
        lines = [line.strip() for line in open(filename)]
        cleaned = 0
        #remove all white spaces from each line and then filter out the danger
        for line in lines:
            line = re.sub(r'\s+', '', line)
            for danger in dangers:
                if danger in line:
                    print "Error : Potential threat detected !"
                    print "Line  : "+line
                    S.safe = False
                    S.save()
                    cleaned +=1
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
'''def execution_engine(code_name, lang, compiled,submissionid,problemid,foldername):
    if compiled == 0 :
        print "\nStage 2 : Not compiled terminated ..."
        return 0
    print "\nStage 2 : Execution started ..."
    ioeredirect=ioe_redirect_create(submissionid,foldername,problemid)
    starttime = time.time()
    running = 1
    if   lang == "C"    :  os.system('LD_PRELOAD='+BASE_PATH+'/EasySandbox/EasySandbox.so '+code_name+ioeredirect+' -nostdlib')
    elif lang == "C++"  :  os.system('LD_PRELOAD='+BASE_PATH+'/EasySandbox/EasySandbox.so '+code_name+ioeredirect+' -nostdlib')
    running = 100
    endtime = time.time()
    timediff = endtime-starttime
    c = Submission.objects.get(id=submissionid)
    c.timetaken = timediff
    c.save()
    print "\nThread completed ! "
    print "Stage 2 : execution completed in : " 
    os.system("rm "+code_name)
    print timediff
    return 0'''


#force killing of a thread after Timelimit for the problem.
def kill(code_name,lang,submissionid,problemid,foldername,userid):
    ioeredirect=ioe_redirect_create(submissionid,foldername,problemid)
    ioeredirect_list=ioeredirect[1:].split(' ')
    arg=[code_name,'-nostdlib']
    prob = Problem.objects.get(id = problemid)
    timelimit=prob.timelimit
    p = SandboxExec(arg,ioeredirect_list)
    p.run(timeout=timelimit,submissionid=submissionid)
    time.sleep(timelimit+0.5)
    c = Submission.objects.get(id=submissionid)
    if c.status == "Timeout":
        return
    thread3 = solution_verificationThread(3, "Thread-SolVerification", 3,str(submissionid), str(problemid),str(foldername),userid)
    thread3.start()
    return False

def clean(file):
    f=open(file,'r+')
    lines = f.read().split("\n")
    f.seek(0,0)
    for i in lines:
        if i:
            f.write(i+'\n');
    f.truncate()
    f.close()
    f=open(file,'r')
    str=f.read()
    f.close()
    print str

def solution_verification(submissionid, problemid,foldername,userid):
    solutionpath = str(BASE_PATH)+"/mainapp/media/question_"+problemid+"/output.txt"
    playeroutputpath = str(BASE_PATH)+"/mainapp/media"+foldername+"/output-"+submissionid+".txt"
    playererrorpath = str(BASE_PATH)+"/mainapp/media"+foldername+"/error-"+submissionid+".txt"
    with open(playererrorpath, 'r') as f:
        lines = f.read().splitlines(True)
    print os.path.getsize(playeroutputpath)
    if os.path.getsize(playeroutputpath)>250000:
        c = Submission.objects.get(id=submissionid)
        if len(lines)>1:
            c.status = "Unsafe Code"
        else:
            c.status = "Timeout"
        c.save()
        pl = Player.objects.get(userid_id=userid)
        pl.totalsubmissions = pl.totalsubmissions + 1
        pl.save()
        return
        
    if len(lines)>1:
        c = Submission.objects.get(id=submissionid)
        c.status = "Unsafe Code"
        c.safe = False
        c.save()
        pl = Player.objects.get(userid_id=userid)
        pl.totalsubmissions = pl.totalsubmissions + 1
        pl.save()
        return
        
    S = Submission.objects.get(id=submissionid)
    with open(playeroutputpath, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(playeroutputpath, 'w') as fout:
        fout.writelines(data[1:])
    clean(playeroutputpath)
    if filecmp.cmp(solutionpath, playeroutputpath):
        pl = Player.objects.get(userid_id=userid)
        pl.totalsubmissions = pl.totalsubmissions + 1
        pl.totalsolutions = pl.totalsolutions + 1
        pr = Problem.objects.get(id=problemid)
        pl.totalscore = pl.totalscore+pr.score
        pl.lastsolutiontime = datetime.now() 
        pl.save()
        S.score = pr.score
        S.status = "Success"
    else:
        pl = Player.objects.get(userid_id=userid)
        pl.totalsubmissions = pl.totalsubmissions + 1
        pl.save()
        S.status = "Failed testcases"
    S.save()
