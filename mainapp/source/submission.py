from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from judge.source.judge import compilation_engine,killThread,cleaner
from mainapp.models import Player,Submission
import re
import sys
import os
import logging
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

ext_to_lang_dict = {
                    "cpp":"C++",
                    "c":"C",
                    "java":"Java",
                    "py":"Python",
                    }
lang_dict = {
                    "C++":".cpp",
                    "C":".c",
                    }
    

def file_verify(file):
    ONE_MB = 1.049e+6
    if len(file)>ONE_MB:
        return False
    else:
        return True
    
def save_submission(request,problemid,lang):
    file = str(request.POST.get('code'))
    if Submission.objects.filter(problemid_id=problemid).filter(status="Success").filter(playerid__userid=request.user).exists():
        return "Already solved, submission not accepted."
    print "here"
    
    if file is None or file=='':
        return False
    if file_verify(file) is False:
        return "File too large"
    foldername = str(request.user.username)+'_'+str(request.user.id)+'/'        
    if True:
        player = Player.objects.get(userid=request.user)
        s =Submission(playerid=player,problemid_id=problemid,language=lang)
        print "saved"
        s.save()
        with open(str(BASE_PATH)+'/media/'+foldername+'s'+str(s.id)+lang_dict[lang], 'wb+') as fin:
            fin.write(file)
        player = Player.objects.get(userid=request.user)
        return s.id
    else:
        return 0

def compile_submission(request,submissionid,problemid,lang):
    filename = 's'+submissionid
    foldername = '/'+str(request.user.username)+'_'+str(request.user.id)
    file = str(BASE_PATH)+'/media'+foldername+'/'+filename

    print file
    cleaner(file, lang, submissionid)
    S = Submission.objects.get(id=submissionid)
    print "hereman"
    if compilation_engine(file,lang,submissionid,problemid,foldername)==1 and S.safe==True:
        thread1 = killThread(1, "Thread-kill", 1,str(file),str(lang),submissionid,problemid,str(foldername),request.user.id)
        thread1.start()
        return "Queued for execution"
    elif S.safe==False:
        S.status = "Unsafe Code, could not execute."
        S.save()
        return "Error, did not execute"
    else:
        S.status = "Compilation Error"
        S.save()
        return "Compilation Error"
