from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def feed(request):
	return render(request, 'feed.html')
