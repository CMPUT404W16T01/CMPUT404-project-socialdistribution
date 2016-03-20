from feed.models import Post, Author, Comment, Friend
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from feed.models import Author
from django.contrib.auth.models import User
import requests
import json



@login_required
# Create your views here.
def friends(request):
	user_object = User.objects.get(username = request.user.username)
	author_object = Author.objects.get(email = user_object)
	friend_requests = Friend.objects.filter(followed_id=author_object.id)
	following = Friend.objects.filter(follower_id=author_object.id)

	all_authors = Author.objects.all()

	# send request to other servers to load their friends
	foreign_authors = {'authors':[]}
	try:
		r = requests.get('http://localhost:8001/api/authors', auth=("admin", "pass"))
		foreign_authors = json.loads(r.text)
	except:
		pass


	context = {
		'authors': all_authors,
		'current_author': author_object,
		'friend_requests': friend_requests,
		'foreign_authors': foreign_authors['authors'],
	}
	return render(request, 'friends.html', context)
