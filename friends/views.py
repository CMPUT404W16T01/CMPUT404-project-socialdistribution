from feed.models import Post, Author, Comment, Friend
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from feed.models import Author
from django.contrib.auth.models import User
import urllib2, base64
import requests
import json



@login_required
# Create your views here.
def friends(request):
	user_object = User.objects.get(username = request.user.username)
	author_object = Author.objects.get(email = user_object)
	# gets 
	followed_by = Friend.objects.filter(followed_id=author_object.id)
	following = Friend.objects.filter(follower_id=author_object.id)

	all_authors = Author.objects.all()

	friend_requests = list()
	my_friends = list()

	# Get all friends if they're local
	for i in followed_by:
		# if the followed_id == the use id, then add them to our list
		if (author_object.id == i.followed_id):
			req = urllib2.Request("http://ditto-test.herokuapp.com/api/friends/%s/%s" % (str(i.follower_id), str(i.followed_id)))

			base64string = base64.encodestring('%s:%s' % ("admin", "pass")).replace('\n', '')
			req.add_header("Authorization", "Basic %s" % base64string) 

			response = urllib2.urlopen(req).read()
			loaded = json.loads(response)
			print "did ditto-test request"
			# friend is local
			try:
				friend = Author.objects.get(id=i.follower_id)
				print "Friend:"
				print friend
			# friend is foreign
			except:
				print i.follower_id
				print i.followed_id
				url = "http://mighty-cliffs-82717.herokuapp.com/api/author/%s" % str(i.follower_id)
				req = urllib2.Request("http://mighty-cliffs-82717.herokuapp.com/api/author/%s" % str(i.follower_id))
				print "attempting mighty request"
				response = urllib2.urlopen(req).read()
				print "Response: "
				print response
				loaded = json.loads(response)
				#print loaded['id']
				friend = loaded

			if friend.id != author_object.id and not loaded.get('friends'):
				friend_requests.append(friend)
			else:
				my_friends.append(friend)

	# For host in hosts:
		# Grab all authors on their server
			# If an author id matches the follower_id in one of our friend requests
				# Append that person to friend_requests

	# send request to other servers to load their friends
	foreign_authors = {'authors':[]}
	try:
		r = requests.get('http://mighty-cliffs-82717.herokuapp.com/api/authors')
		#print r.text

		#r = requests.get('http://localhost:8001/api/authors', auth=("admin", "pass"))

		foreign_authors = json.loads(r.text)
	except Exception as e:
		print e
		pass


	context = {
		'authors': all_authors,
		'current_author': author_object,
		'friends': my_friends,
		'friend_requests': friend_requests,
		'foreign_authors': foreign_authors['authors'],
	}

	return render(request, 'friends.html', context)
