from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from judge.source.judge import compilation_engine,execution_engine,kill,killThread,execThread,cleaner
from mainapp.models import Player,Submission
import re
import sys

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
    pattern = re.compile('[a-zA-Z0-9]+\.[c|cpp|CPP|c++|cp|cxx|C|py|java]')
    match = pattern.match(file.name)
    if match:
        return True
    else:
        return False

def save_submission(request,problemid):
    file = request.FILES.get('file')
    filename = str(file)
    if file is None:
        return False
    if file_verify(file) is False:
        return False
    foldername = str(request.user.username)+'_'+str(request.user.id)+'/'        
    try:
        with open('mainapp/media/'+foldername+str(file), 'wb+') as destination:
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
    file = 'mainapp/media'+foldername+'/'+filename
    lang = ext_to_lang_dict[extension]
    cleaner(file, lang)
    print file
    if compilation_engine(file,lang,submissionid,problemid,foldername)==1:
        thread1 = killThread(1, "Thread-kill", 1,file,lang,submissionid)
        thread2 = execThread(2, "Thread-exec", 2,file,lang,submissionid,problemid,foldername)
        thread1.start()
        thread2.start()
        return "Queued for execution"
    else:
        return "Compilation Error"
    