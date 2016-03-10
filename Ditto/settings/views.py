from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from feed.models import Post
from feed.models import Author
from django.contrib.auth.models import User
from django.template import Context, loader, Template
import uuid
import json
import datetime

@login_required
def settings(request):
	user_object = User.objects.get(username=request.user.username)
	author_object = Author.objects.get(email=user_object)

	# display name
	display_name = author_object.display_name

	# github account
	github_account = author_object.github_account

	# github flag
	github_flag = author_object.github_flag
	if github_flag:
		github_flag = 'checked'

	context = {
		'display_name': display_name,
		'github_account': github_account,
		'github_flag': github_flag,
	}

	return render(request, 'settings.html', context)