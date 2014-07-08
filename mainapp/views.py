from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from source.submission import *
from source.login import *
from source.player import *

def index(request):
    return render_to_response("index.html")

def login(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append('Enter username.')
        if not request.POST.get('password', ''):
            errors.append('Enter a passowrd.')
        if not errors:
            if authenticate_user(request):
                return HttpResponseRedirect('/home/')
            else:
                if errors ==[]:
                    errors.append('Invalid Credentials')  
    c = {'errors' : errors}
    c.update(csrf(request))
    return render_to_response("player-login.html",c)

@login_required(login_url='/login/')
def home(request):
    c={}
    if request.FILES:
        c['messages']=submit_program(request)
    files=get_player_submissions(request)
    c['files']=files
    c['user']=request.user.username
    c.update(csrf(request))
    return render_to_response("home.html",c,context_instance=RequestContext(request))

@login_required(login_url='/login/')
def submit_program(request):
    if save_submission(request):
        return 'success'
    else:
        return 'failed'    

def logout(request):
    logout_player(request)
    return HttpResponseRedirect('/index/')

def signup(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append('Enter username.')
        if not request.POST.get('password', ''):
            errors.append('Enter a password.')
        if not request.POST.get('name', ''):
            errors.append('Enter a name.')
        if not request.POST.get('email', ''):
            errors.append('Enter an email.')
        if not request.POST.get('college', ''):
            errors.append('Enter a college.')
        if not errors:
            if register_player(request.POST):
                return HttpResponseRedirect('/login/')
            else:
                errors.append('Error, Try again')
    c = {'errors' : errors}
    c.update(csrf(request))

    return render_to_response("signup.html",c,context_instance=RequestContext(request))

