# from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


def index(request):
    if request.user.is_authenticated():
        pass
    else:
        return render(request, 'signin.html', {'account_status': 'notlogged'})


def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'index.html', {'account_status': 'active'})
        else:
            return render(request, 'signin.html', {'account_status': 'inactive'})
    else:
        return render(request, 'signin.html', {'account_status': 'invalid'})


def search(request):
    pass


def list(request):
    pass
