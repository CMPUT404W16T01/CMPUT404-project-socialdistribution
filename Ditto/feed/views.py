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
import CommonMark
# Create your views here.

@login_required
def feed(request):
	user_object = User.objects.get(username = request.user.username)
	author_object = Author.objects.get(email = user_object)
	self_posts = Post.objects.filter(author_id = author_object)
	public_posts = Post.objects.filter(visibility = "public")
    #friend_posts
    #foaf_posts
	server_posts = Post.objects.filter(visibility = "server")
	all_posts = self_posts | public_posts | server_posts
	for post in all_posts:
		#print post.post_id
		if (str(author_object.user_id) == str(post.author_id)):
			post.flag=True
		else:
			post.flag=False
	

	context = {
		'all_posts': all_posts,
	}
	return render(request, 'feed.html', context)


def delete(request):
	post_id = request.POST.get('post_post_id')
	Post.objects.filter(post_id = post_id).delete()
	return redirect('/feed')


def logout(request):
	auth_logout(request)
	return redirect('/login')


def create_post(request):
	body = request.POST.get('post_body')
	date_published = datetime.datetime
	is_markdown = json.loads(request.POST.get('is_markdown'))
	if is_markdown:
		body = CommonMark.commonmark(body)
	visibility = request.POST.get('visibility')
	c_username = request.user.username
	user_object = User.objects.get(username = c_username)
	author_object = Author.objects.get(email = user_object)

	DITTO_HOST = request.get_host()
	title = request.POST.get('title')
	description = request.POST.get('description')

	categories = request.POST.get('categories')
	
	c= categories.split(' ')
	
	categories_json = json.dumps(c)
	

	new_post = Post(date_published = date_published, author_id = author_object, body = body, is_markdown = is_markdown, visibility = visibility, source= DITTO_HOST, origin = DITTO_HOST, categories=categories,title=title,description=description ) 
	new_post.save()

	return HttpResponse(request.POST.get('post_body'))