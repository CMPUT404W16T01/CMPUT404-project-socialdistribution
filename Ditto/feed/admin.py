from django.contrib import admin
from .models import Author, Post, Comment, Friend

# Register your models here.
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friend)
