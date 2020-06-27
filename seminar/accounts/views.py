from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Profile

# Create your views here.
def signup(request):
    if request.method  == 'POST':
        if request.POST['password_1'] == request.POST['password_2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password_1'])
            user.profile.college = request.POST['college']
            user.profile.major = request.POST['major']
            user.profile.age = request.POST['age']
            auth.login(request, user)
            return redirect('/feeds')
    return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/feeds')
        else:
            return render(request, 'accounts/login.html', {'error' : 'username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    return render(request, 'accounts/logout.html')