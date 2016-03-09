from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from feed.models import Post
from feed.models import Author
from django.contrib.auth.models import User
from django.template import Context, loader
import uuid
import json
import datetime
# Create your views here.

@login_required
def feed(request):
	return render(request, 'feed.html')

def create_post(request):
	body = request.POST.get('post_body')
	date_published = datetime.datetime
	is_markdown = json.loads(request.POST.get('is_markdown'))
	visibility = request.POST.get('visibility')
	c_username = request.user.username
	user_object = User.objects.get(username = c_username)
	author_object = Author.objects.get(email = user_object)


	print "date :" + str(date_published) + "\n" + "post body :" + body + "\n" + "is markdown : " + str(is_markdown) + "\n" + "visibility : " + visibility 
	

	new_post = Post(date_published = date_published, author_id = author_object, body = body, is_markdown = is_markdown, visibility = visibility)
	
	new_post.save()

	return HttpResponse(request.POST.get('post_body'))
