import django
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.contrib.auth.models import User
import os
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


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


class Git_Post(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=500, default=" ")
    date = models.CharField(max_length=500, default=" ")
    link = models.CharField(max_length=500, default=" ")


# @python_2_unicode_compatible
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author)  # issue here?
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


class CommentAuthor(models.Model):
    comment_author_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.UUIDField(editable=False)
    host = models.URLField(max_length=500)
    displayName = models.CharField(max_length=60)
    url = models.CharField(max_length=500)
    github = models.CharField(max_length=30)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_id = models.ForeignKey(Post)
    author = models.ForeignKey(CommentAuthor)
    author_name = models.CharField(max_length=1000, default=" ")
    comment = models.CharField(max_length=1000)
    contentType = models.CharField(max_length=50, default=" ")  # not in user stories, but in json spec???
    published = models.DateTimeField(default=django.utils.timezone.now)
    image = models.ImageField(blank=True)

    def __unicode__(self):
        return str(self.id)


class Friend(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    follower_host = models.URLField(max_length=500)
    follower_id = models.UUIDField()
    followed_host = models.URLField(max_length=500)
    followed_id = models.UUIDField()

# @python_2_unicode_compatible
class ForeignHost(models.Model):
    foreign_username = models.ForeignKey(User)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=60)
    url = models.CharField(primary_key=True, max_length=500)

    def __unicode__(self):
        return str(self.url)

class Img(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    #actual_image = models.ImageField(upload_to ='images/' os.path.join("images"))
    actual_image = models.ImageField(upload_to ='images/')
    parent_post = models.ForeignKey(Post)

    def __unicode__(self):
        return str(self.id)

#taken from darrinm at
#http://stackoverflow.com/questions/5372934/how-do-i-get-django-admin-to-delete-files-when-i-remove-an-object-from-the-datab
@receiver(pre_delete, sender=Img)
def img_delete(sender, instance, **kwargs):
    instance.actual_image.delete(False)