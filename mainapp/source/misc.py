from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from mainapp.models import Problem,Player,PlayerProblemViewTime
from judge.source.judge import clean

import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

def authenticate_user(data,request):
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
    p = Problem(name=request.POST['title'],description=request.POST['description'],difficulty=request.POST['difficulty'],
                timelimit = request.POST['timelimit'], score = request.POST['score']
                )
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
    clean(str(BASE_PATH)+'/media/'+foldername+'output.txt')
    file = request.FILES.get('testcases') 
    with open(str(BASE_PATH)+'/media/'+foldername+'testcases.txt', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    clean(str(BASE_PATH)+'/media/'+foldername+'testcases.txt')
    file = request.FILES.get('simpleoutput') 
    with open(str(BASE_PATH)+'/media/'+foldername+'simpleoutput.txt', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    clean(str(BASE_PATH)+'/media/'+foldername+'simpleoutput.txt')
    file = request.FILES.get('simpleinput') 
    with open(str(BASE_PATH)+'/media/'+foldername+'simpleinput.txt', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    clean(str(BASE_PATH)+'/media/'+foldername+'simpleinput.txt')
    return True

def get_problems():
    p = Problem.objects.all()
    prob = []
    prob0 = {'id':p[0].id,'name':p[0].name,'desc':p[0].description,'participants':p[0].player_set.count(),'score':p[0].score,
             'difficulty':p[0].difficulty
             }
    if len(p)==1:
        return [prob0,[]]
    else:
        p=p.exclude(id=p[0].id)
    for i in p:
        data = {'id':i.id,'name':i.name,'desc':i.description,'participants':i.player_set.count(),'score':i.score,'difficulty':i.difficulty}
        prob.append(data)
    return [prob0,prob]

def get_problem_details(id):
    p = Problem.objects.get(id=id)
    f=open(BASE_PATH+'/media/question_'+str(p.id)+'/simpleinput.txt')
    input=f.read()
    f.close()
    f=open(BASE_PATH+'/media/question_'+str(p.id)+'/simpleoutput.txt')
    output=f.read()
    f.close()
    
    data = {'id':p.id,'name':p.name,'desc':p.description,'participants':p.player_set.count(),'score':p.score,'difficulty':p.difficulty,
            'input':input,'output':output,'timelimit':p.timelimit
            }
    return data

def leaderboard():
    leaderboard = []
    players = Player.objects.all()
    for player in players:
        data = {"name" : player.userid.username, "score" : player.totalscore,'lastsolution':player.lastsolutiontime}
        leaderboard.append(data)
    return leaderboard