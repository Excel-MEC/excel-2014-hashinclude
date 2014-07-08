from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import re
import sys

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

def save_submission(request):
    file = request.FILES.get('file')
    if file is None:
        return False
    if file_verify(file) is False:
        return False
    foldername = str(request.user.username)+'_'+str(request.user.id)+'/'
    try:
        with open('mainapp/media/'+foldername+str(file), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return True
    except:
        return False

