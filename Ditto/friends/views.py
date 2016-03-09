from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def friends(request):
	return render(request, 'friends.html')
