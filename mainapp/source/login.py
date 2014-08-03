from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
import os

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