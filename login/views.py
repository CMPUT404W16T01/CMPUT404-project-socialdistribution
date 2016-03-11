from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from feed.models import Author


# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return redirect('/feed')
    else:
        return render(request, 'login.html')


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        user_object = User.objects.get(username=username)
        author_object = Author.objects.get(email=user_object)
        print author_object.admin_auth
        if user and author_object.admin_auth:
            auth_login(request, user)
            return redirect('/feed')
        else:
            return redirect('/register/confirm')
