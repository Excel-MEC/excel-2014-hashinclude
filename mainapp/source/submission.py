from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from judge.source.judge import compilation_engine,execution_engine,kill,killThread,execThread
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
        player = Player.object.get(userid=request.user.id)
        s =Submission(playerid=player.id,problemid=request.session.get('problemid','None'),language=ext_to_lang_dict[filename[filename.find('.')+1:]])
        if request.session.get('problemid'):
            del request.session['problemid']
        s.save()
        return s.id
    except:
        return 0

def compile_submission(request,submissionid):
    filename = str(request.FILES.get('file'))
    extension = filename[filename.find('.')+1:]
    file = 'mainapp/media/'+str(request.user.username)+'_'+str(request.user.id)+'/'+filename
    cleaner(file, ext_to_lang_dict[extension])
    if compilation_engine(file,ext_to_lang_dict[extension])==1:
        thread1 = killThread(1, "Thread-kill", 1,file,lang,submissionid)
        thread2 = execThread(2, "Thread-exec", 2,file,lang,submissionid)
        thread1.start()
        thread2.start()
        return "Queued for execution"
    else:
        return "Compilation Error"
    