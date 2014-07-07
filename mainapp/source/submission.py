from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def save_submission(request):
    file = request.FILES.get('file')
    if file is None:
        return False
    foldername = str(request.user.username)+'_'+str(request.user.id)+'/'
    try:
        with open('mainapp/media/'+foldername+str(file), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return True
    except:
        return False

