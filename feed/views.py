from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from feed.models import Post
from feed.models import Git_Post
from feed.models import Author
from feed.models import Comment
from django.contrib.auth.models import User
from django.template import Context, loader, Template
import uuid
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
import CommonMark
import urllib2
import feedparser
from dateutil.parser import parse
from datetime import datetime


# Create your views here.

@login_required
def feed(request):
    user_object = User.objects.get(username=request.user.username)
    author_object = Author.objects.get(email=user_object)

    github_name = "".join((author_object.github).split())

    github_posts = create_github_post(github_name)

    # My feed, access all posts that I can see
    self_posts = Post.objects.filter(author_id=author_object)
    public_posts = Post.objects.filter(visibility="PUBLIC")
    all_comments = Comment.objects.all()
    # friend_posts
    # foaf_posts
    server_posts = Post.objects.filter(visibility="SERVER ONLY")
    main_posts = self_posts | public_posts | server_posts
    for post in main_posts:
        # print post.id
        comment_list = []
        if (str(author_object.id) == str(post.author)):
            post.flag = True
        else:
            post.flag = False

        for comment in all_comments:
            if (str(comment.post_id) == str(post.id)):
                comment_list.append(comment)
        post.comments = comment_list
        print post.comments
    # end of my feed

    # Begin Public Feed
    # public_posts was already created for use in the other one
    for post in public_posts:
        comment_list = []

        # print post.id
        if (str(author_object.id) == str(post.author)):
            post.flag = True
        else:
            post.flag = False

        for comment in all_comments:
            if (str(comment.post_id) == str(post.id)):
                comment_list.append(comment)
        post.comments = comment_list
    # end of public feed

    # Begin My Posts
    # self_posts was already created for use
    for post in self_posts:
        comment_list = []

        # print post.id
        if (str(author_object.id) == str(post.author)):
            post.flag = True
        else:
            post.flag = False

        for comment in all_comments:
            if (str(comment.post_id) == str(post.id)):
                comment_list.append(comment)
        post.comments = comment_list
    # end of public feed




    context = {
        'main_posts': main_posts,
        'public_posts': public_posts,
        'my_posts': self_posts,
        "github_posts": github_posts,
    }

    return render(request, 'feed.html', context)

def create_github_post(github_id):
    d = feedparser.parse("https://github.com/" + github_id + ".atom")
    items = d["items"]
    git_feed = []
    for item in items:
        date = item["date"]
        time = (parse(date).time()).strftime("%I:%M %p")
        display_date = ((parse(date).date()).strftime("%B %d, %Y at " + time))
        new_git_post = Git_Post(title=item["title"], date=display_date, link=item["link"])
        git_feed.append(new_git_post)
    return git_feed


def profile(request):
    user_object = User.objects.get(username=request.user.username)
    author_object = Author.objects.get(email=user_object)
    return redirect('/author/' + str(author_object.id) + '/profile')


def get_profile(request, pk):
    user_object = User.objects.get(username=request.user.username)
    us_object = Author.objects.get(email=user_object)
    them_object = Author.objects.get(id=pk)

    context = {
        'sender': us_object,
        'them': them_object,
    }

    return render(request, 'profile.html', context)


def delete(request):
    id = request.POST.get('post_id')
    Post.objects.filter(id=id).delete()
    return redirect('/feed')


def logout(request):
    auth_logout(request)
    return redirect('/login')


def create_comment(request):
    # text/x-markdown
    # text/plain
    comment = request.POST.get('comment-input')
    parent_id = request.POST.get('comment-parent-id')
    is_markdown = request.POST.get('comment-is-markdown')

    if is_markdown:
        comment = CommonMark.commonmark(comment)
        is_markdown = True
    else:
        is_markdown = False

    post_object = Post.objects.get(id=parent_id)
    c_username = request.user.username
    user_object = User.objects.get(username=c_username)
    author_object = Author.objects.get(email=user_object)
    author_name = author_object.displayName

    # new_comment = Comment(author_id = author_object, id = post_object, comment = comment, is_markdown = is_markdown, published=published)
    # print("comment made")


    packet = {}
    packet['comment'] = comment
    if is_markdown:
        packet['contentType'] = 'text/x-markdown'
    else:
        packet['contentType'] = 'text/plain'
    packet['published'] = str(datetime.now())
    packet['author'] = {}
    packet['author']['id'] = str(author_object.id)
    packet['author']['host'] = request.get_host()
    packet['author']['displayName'] = author_object.displayName
    packet['author']['url'] = author_object.url
    packet['author']['github'] = "http://github.com/" + author_object.github

    json_packet = json.dumps(packet)
    # print json_packet
    url1 = "http://" + request.get_host() + "/api/posts/" + parent_id + "/comments/"#?id=" + str(author_object.id)
    req = urllib2.Request(url1)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Basic YWRtaW46cGFzcw==')
    urllib2.urlopen(req, json_packet)
    # new_comment.save()
    return redirect('/feed')


def create_post(request):
    content = request.POST.get('post_body')
    published = datetime.now()
    is_markdown = json.loads(request.POST.get('is_markdown'))
    if is_markdown:
        contentType = "text/x-markdown"
        content = CommonMark.commonmark(content)
    else:
        contentType = "text/plain"

    visibility = request.POST.get('visibility')
    c_username = request.user.username
    user_object = User.objects.get(username=c_username)
    author_object = Author.objects.get(email=user_object)
    author_name = author_object.displayName

    DITTO_HOST = request.get_host()
    title = request.POST.get('title')
    description = request.POST.get('description')

    categories = request.POST.get('categories')

    c = categories.split(' ')

    categories_json = json.dumps(c)

    new_post = Post(published=published, author=author_object, content=content, contentType=contentType,
                    visibility=visibility, source=DITTO_HOST, origin=DITTO_HOST, categories=categories, title=title,
                    description=description)
    new_post.save()

    return HttpResponse(request.POST.get('post_body'))
