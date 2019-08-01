from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login, authenticate

from django.http import HttpResponse


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return redirect('home')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            # return HttpResponse('로그인 실패. 다시 시도 해보세요.')
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request) : 
        if request.method == 'POST' :
            auth.logout(request)
            redirect('/')
        return redirect('/')    