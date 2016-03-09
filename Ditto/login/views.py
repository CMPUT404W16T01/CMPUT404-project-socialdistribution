from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import login as auth_login, authenticate



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
		if user:
			auth_login(request, user)
			return redirect('/feed')
		else:
			return redirect('/login')
