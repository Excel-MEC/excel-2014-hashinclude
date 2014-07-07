from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from mainapp.models import Player
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
    try:
        p = Player(userid=user,name=data['name'],email=data['email'],college=data['college'])
        p.save()
        newpath = DIR + '/' + str(user.username)+ '_'+ str(user.id)
        if not os.path.exists(newpath): os.makedirs(newpath)
        print "Success"
        
        return True
    except:
        try:
            p.delete()
            user.delete()
            return False
        except:
            try:
                user.delete()
                return False
            except:
                return False
    
def logout_player(request):
    logout(request)

def get_player_submissions(request):
    DIR = os.path.dirname(os.path.dirname(__file__)) + '/media'
    path = DIR+'/'+str(request.user.username)+'_'+str(request.user.id)  
    allfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    return allfiles
    

    