from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from mainapp.models import Player,Submission,PlayerProblemViewTime,Problem
import os

def register_player(data):
    DIR = os.path.dirname(os.path.dirname(__file__)) + '/media'
    user = User(username=data['username'])
    user.first_name = data['name']
    user.username = data['username']
    user.set_password(data['password'])
    try:
        user.save()
    except:
        return False
    if True:
        p = Player(userid=user,name=data['name'],email=data['email'],college=data['college'],fbuserid=data.get('id','N/A'))
        p.save()
        newpath = DIR + '/' + str(user.username)+ '_'+ str(user.id)
        if not os.path.exists(newpath): os.makedirs(newpath)
        print "Success"
        
        return True
    else:
        try:
            p.delete()
            user.delete()
            print "both"
            return False
        except:
            try:
                user.delete()
                print "user"
                return False
            except:
                return False
    
def logout_player(request):
    if request.session.get('playerid','') != '':
        del request.session['playerid']
    logout(request)

def get_player_submissions(request):
    submissions = []
    p = Player.objects.get(userid=request.user)
    all = Submission.objects.filter(playerid=p)
    for s in all:
        data = {"status":s.status,'problemname':s.problemid.name,'score':s.score,'timestamp':s.timestamp}
        submissions.append(data)
    
    return submissions

def get_player_profile(request):
    profile = {}
    p = Player.objects.get(userid_id=request.user.id)
    if p.totalsubmissions == 0:
        denominator = 1
    else:
        denominator = p.totalsubmissions
    print p.totalsubmissions,p.totalsolutions
    profile = {"name" : request.user.username, "email" : p.email, "totalscore":p.totalscore, "successrate":(float(p.totalsolutions)/denominator)*100,
               "totalsubmissions" : p.totalsubmissions, "wrongsolutions":p.totalsubmissions-p.totalsolutions, "totalsolutions":p.totalsolutions,
               "problemsviewed" : p.problems_viewed.count()
               }
    
    return profile

def update_views(playerid,problemid):
    try:
        player=Player.objects.filter(problems_viewed__id=problemid).filter(id=playerid)
        print player
        if len(player)==1:
            print "he"
            return
        else:
            raise Exception
    except:
        player = Player.objects.get(id=playerid)
        problem = Problem.objects.get(id=problemid)
        player.problems_viewed.add(problem)
        player.save()
        ppv=PlayerProblemViewTime(playerid=player,problemid=problem)
        ppv.save()

def get_player_id(userid):
    p = Player.objects.get(userid_id=userid)
    return p.id
    
