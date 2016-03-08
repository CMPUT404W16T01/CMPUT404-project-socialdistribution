from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid

# Create your models here.
#@python_2_unicode_compatible
class Author(models.Model):
	display_name	= models.CharField(max_length=60)
	password		= models.CharField(max_length=30)
	email			= models.EmailField(max_length=50)
	bio				= models.CharField(max_length=1000)
	host			= models.URLField(max_length=500)
	github_account	= models.CharField(max_length=30)
	github_flag		= models.BooleanField(default=False)
	user_id			= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	admin_auth      = models.BooleanField(default=False)

#@python_2_unicode_compatible
class Post(models.Model):
	post_id			= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author_id		= models.ForeignKey(Author)	# issue here?
	date_published	= models.DateTimeField(auto_now=True) # issue here?
	body			= models.CharField(max_length=1000)
	is_markdown		= models.BooleanField(default=False)
	visibility		= models.CharField(max_length=20)
	image			= models.ImageField()


class Comment(models.Model):
	comment_id		= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	post_id			= models.ForeignKey(Post) # issue?
	author_id		= models.ForeignKey(Author) # issue?
	body			= models.CharField(max_length=1000)
	is_markdown		= models.BooleanField(default=False) # not in user stories, but in json spec???
	date_published 	= models.DateTimeField(auto_now=True)


class Friend(models.Model):
	follower_id		= models.UUIDField(primary_key=True)
	followed_id		= models.UUIDField()

