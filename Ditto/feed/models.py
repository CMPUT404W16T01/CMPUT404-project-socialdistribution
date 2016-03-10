from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.
#@python_2_unicode_compatible
class Author(models.Model):
	email 			= models.ForeignKey(User)
	user_id			= models.UUIDField(primary_key=True, editable=False)
	display_name	= models.CharField(max_length=60)
	bio				= models.CharField(max_length=1000, default=" ")
	host			= models.URLField(max_length=500)
	github_account	= models.CharField(max_length=30, default=" ")
	github_flag		= models.BooleanField(default=False)
	admin_auth      = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.user_id)

#@python_2_unicode_compatible
class Post(models.Model):
	post_id			= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author_id		= models.ForeignKey(Author)	# issue here?
	date_published	= models.DateTimeField(auto_now=True) # issue here?
	body			= models.CharField(max_length=1000)
	is_markdown		= models.BooleanField(default=False)
	visibility		= models.CharField(max_length=20) #private, public, friends, foaf, server
	image			= models.ImageField(blank=True)
	title			= models.CharField(max_length=50, default=" ")
	source			= models.URLField(default=" ")
	origin			= models.URLField(default=" ")
	description		= models.CharField(max_length=150, default=" ")
	comment_count	= models.IntegerField(default=0)
	categories		= models.CharField(max_length=1000, default=" ")

	def __unicode__(self):
		return str(self.post_id)


class Comment(models.Model):
	comment_id		= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	post_id			= models.ForeignKey(Post) # issue?
	author_id		= models.ForeignKey(Author) # issue?
	body			= models.CharField(max_length=1000)
	is_markdown		= models.BooleanField(default=False) # not in user stories, but in json spec???
	date_published 	= models.DateTimeField(auto_now=True)
	image			= models.ImageField(blank=True)


class Friend(models.Model):
	follower_id		= models.UUIDField(primary_key=True)
	followed_id		= models.UUIDField()

