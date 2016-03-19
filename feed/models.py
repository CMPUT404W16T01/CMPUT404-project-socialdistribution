import django
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
# @python_2_unicode_compatible
class Author(models.Model):
    email = models.ForeignKey(User)
    id = models.UUIDField(primary_key=True, editable=False)
    displayName = models.CharField(max_length=60)
    bio = models.CharField(max_length=1000, default=" ")
    host = models.URLField(max_length=500)
    github = models.CharField(max_length=30, default=" ")
    github_flag = models.BooleanField(default=False)
    admin_auth = models.BooleanField(default=False)
    url = models.CharField(max_length=500, default=" ")

    def __unicode__(self):
        return str(self.id)


# @python_2_unicode_compatible
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author)  # issue here?
    published = models.DateTimeField(default=django.utils.timezone.now)  # issue here?
    content = models.CharField(max_length=1000)
    contentType = models.CharField(max_length=50, default=" ")
    visibility = models.CharField(max_length=20)  # private, public, friends, foaf, server
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=50, default=" ")
    source = models.URLField(default=" ")
    origin = models.URLField(default=" ")
    description = models.CharField(max_length=150, default=" ")
    count = models.IntegerField(default=0)
    categories = models.CharField(max_length=1000, default=" ")

    def __unicode__(self):
        return str(self.id)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.ForeignKey(Post)  # issue?
    author = models.CharField(max_length=2000, default="")  # issue?
    author_name = models.CharField(max_length=1000, default=" ")
    comment = models.CharField(max_length=1000)
    contentType = models.CharField(max_length=50, default=" ")  # not in user stories, but in json spec???
    published = models.DateTimeField(default=django.utils.timezone.now)
    image = models.ImageField(blank=True)

    def __unicode__(self):
        return str(self.id)


class Friend(models.Model):
    follower_host = models.URLField(max_length=500)
    follower_id = models.UUIDField(primary_key=True)
    followed_host = models.URLField(max_length=500)
    followed_id = models.UUIDField()


class ForeignHost(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=60)
    url = models.CharField(max_length=500)