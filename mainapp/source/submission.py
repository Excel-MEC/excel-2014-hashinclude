from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from judge.source.judge import compilation_engine,execution_engine,kill,killThread,execThread,cleaner
from mainapp.models import Player,Submission
import re
import sys
import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

ext_to_lang_dict = {
                    "cpp":"C++",
                    "c":"C",
                    "java":"Java",
                    "py":"Python",
                    }
    

def file_verify(file):
    ONE_MB = 1.049e+6
    if file.size>ONE_MB:
        return False
    pattern = re.compile('[a-zA-Z0-9]+\.[c|cpp|CPP|c++|cp|cxx|C]')
    match = pattern.match(file.name)
    if match:
        return True
    else:
        return False

def save_submission(request,problemid):
    file = request.FILES.get('file')
    if Submission.objects.filter(problemid_id=problemid).filter(status="Success").filter(playerid__userid=request.user).exists():
        return "Already solved, submission not accepted."
    
    filename = str(file)
    if file is None:
        return False
    if file_verify(file) is False:
        return False
    foldername = str(request.user.username)+'_'+str(request.user.id)+'/'        
    try:
        with open(str(BASE_PATH)+'/media/'+foldername+str(file), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        player = Player.objects.get(userid=request.user)
        s =Submission(playerid=player,problemid_id=problemid,language=ext_to_lang_dict[filename[filename.find('.')+1:]])
        s.save()
        return s.id
    except:
        return 0

def compile_submission(request,submissionid,problemid):
    filename = str(request.FILES.get('file'))
    extension = filename[filename.find('.')+1:]
    filename = filename[:filename.find('.')]
    foldername = '/'+str(request.user.username)+'_'+str(request.user.id)
    file = str(BASE_PATH)+'/media'+foldername+'/'+filename
    lang = ext_to_lang_dict[extension]
    cleaner(file, lang)
    if compilation_engine(file,lang,submissionid,problemid,foldername)==1:
        thread1 = killThread(1, "Thread-kill", 1,str(file),str(lang),submissionid,problemid,str(foldername),request.user.id)
        thread1.start()
        return "Queued for execution"
    else:
        S.status = "Compilation Error"
        S.save()
        return "Compilation Error"
