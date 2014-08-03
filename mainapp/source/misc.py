from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from mainapp.models import Problem

import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

def authenticate_user(request):
    data = request.POST
    if not User.objects.all():
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'john')
    user = authenticate(username=data['username'], password=data['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return True
        else:
            return False
    else:
        return False
    
def save_question(request):
    p = Problem(name=request.POST['title'],description=request.POST['description'],difficulty='Intermediate')
    p.save()
    DIR = os.path.dirname(os.path.dirname(__file__)) + '/media'
    newpath = DIR + '/question_' + str(p.id)
    if not os.path.exists(newpath): os.makedirs(newpath)
    data = request.POST
    file = request.FILES.get('output')
    if file is None:
        return False
    foldername = 'question_'+str(p.id)+'/'
    with open(str(BASE_PATH)+'/media/'+foldername+'output.txt', 'wb') as destination:
        for chunk in file.chunks():
              destination.write(chunk)
    file = request.FILES.get('testcases') 
    with open(str(BASE_PATH)+'/media/'+foldername+'testcases.txt', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return True

def get_problems():
    p = Problem.objects.all()
    prob = []
    for i in p:
        data = {'id':i.id,'name':i.name}
        prob.append(data)
    print prob
    return prob

def get_problem_details(id):
    p = Problem.objects.get(id=id)
    data = {'id':id,'name':p.name,'description':p.description}
    return data
