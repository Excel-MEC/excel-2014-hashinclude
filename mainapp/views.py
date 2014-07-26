from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from source.submission import *
from source.misc import *
from source.player import *

def index(request):
    c = {}
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append('Enter username.')
        if not request.POST.get('password', ''):
            errors.append('Enter a passowrd.')
        if not errors:
            if authenticate_user(request):
                print "Entered"
                return HttpResponseRedirect('/home/')
            else:
                if errors ==[]:
                    errors.append('Invalid Credentials')  
    c = {'errors' : errors}
    c.update(csrf(request))
    return render_to_response("index.html",c)

def leaders(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("leaderboard.html",c)

def profile(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("profile.html",c)

def problem(request):
    id = request.GET.get('id')
    details = get_problem_details(id)
    c = {'q': details}
    c.update(csrf(request))
    return render_to_response("problem.html",c)

def allproblems(request):
    details = get_problems()
    c = {'problems': details}
    c.update(csrf(request))
    print "here"
    return render_to_response("allproblems.html",c)

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
    return render_to_response("index.html",c)

@login_required(login_url='/login/')
def home(request):
    c={}
    print "hello", request.user.is_authenticated()
    if request.FILES:
        if c['messages']==submit_program(request):
            c['message_compilation'] = compile_submission(request)
        else:
            c['messages']='failed'
    files=get_player_submissions(request)
    c['files']=files
    c['user']=request.user.username
    c['problems'] = get_problems()
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

