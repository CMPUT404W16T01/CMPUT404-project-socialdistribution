from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from feed.models import Post, Git_Post, Author, Comment, ForeignHost
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
import requests
import base64


# Create your views here.

@login_required
def feed(request):
    #requests.get("")

    their_post_list = []
    try:
        foreign_hosts = ForeignHost.objects.filter()
        for i in foreign_hosts:
            url = i.url + "api/posts"
            req = urllib2.Request(url)
            response = urllib2.urlopen(req).read()
            loaded = json.loads(response)

            their_posts = loaded.get('posts')
            their_post_list = []

            for post in their_posts:
                comments = []
                description = post.get("description")
                title = post.get("title")
                content = post.get("content")
                published_raw = post.get("published")
                origin = post.get("origin")
                id = post.get("id")
                published = datetime.strptime(published_raw, '%Y-%m-%dT%H:%M:%S.%fZ')
                published  = published.replace(tzinfo=None)

                their_comments = post.get("comments")
                if len(their_comments) > 0:
                    for comment1 in their_comments:
                        comment_body = comment1.get('comment')
          
                        comment_author = str(comment1.get('author').get('displayName'))

                        new_comment = Comment(author_name = comment_author, comment = comment_body)
                        comments.append(new_comment)
                new_post = Post( id = id, description = description, title = title, content = content, published = published, origin = origin)
                new_post.comments = comments
                their_post_list.append(new_post)

    except Exception as e:
        print e
        print "couldn't get other hosts posts"



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

    main_posts_list = []
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
        main_posts_list.append(post)
        #print post.comments
    # end of my feed

    main_posts = main_posts_list + their_post_list
    for x in main_posts:
        x.published= x.published.replace(tzinfo=None)
    main_posts.sort(key=lambda x: x.published, reverse=True)



    public_posts_list = []
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
        public_posts_list.append(post)


    public_posts = public_posts_list + their_post_list
    for x in public_posts:
        x.published= x.published.replace(tzinfo=None)
    public_posts.sort(key=lambda x: x.published, reverse=True)

    # end of public feed

    self_posts_list=[]
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
        self_posts_list.append(post)
    # end of public feed


    for x in self_posts_list:
        x.published= x.published.replace(tzinfo=None)
    self_posts_list.sort(key=lambda x: x.published, reverse=True)


    context = {
        'main_posts': main_posts,
        'public_posts': public_posts,
        'my_posts': self_posts_list,
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

    them_object = Author.objects.filter(id=pk)

    if len(them_object) == 0:
        # this means this profile we want to access is a foreign host
        try:
            # TODO: We should be looping all possible hosts here
            foreign_hosts = ForeignHost.objects.filter()
            for i in foreign_hosts:
                # r = requests.get('http://localhost:8001/api/authors', auth=("admin", "pass"))
                url = i.url + "/api/authors"
                if i.username != 'null':
                    r = requests.get(url, auth=(i.username, i.password))
                else:
                    r = requests.get(url)
                foreign_authors = json.loads(r.text)
                for each in foreign_authors['authors']:
                    if each['id'] == pk:
                        them_object = each
                        break
        except:
            # do something maybe
            pass
    else:
        them_object = them_object[0]


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
    is_markdown = request.POST.get('comment-is-markdown',default='off')
    origin = request.POST.get('comment-parent-origin')

    if is_markdown == 'on':
        comment = CommonMark.commonmark(comment)
        is_markdown = True
    else:
        is_markdown = False

    
    #post_object = Post.objects.get(id=parent_id)
    c_username = request.user.username
    user_object = User.objects.get(username=c_username)
    author_object = Author.objects.get(email=user_object)
    #author_name = author_object.displayName
    
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


    # WE COULD USE THIS IF THEY GAVE US ORIGIN INSTEAD OF AN EMPTY STRING
    # "origin":"http://whereitcamefrom.com/api/posts/zzzzz",
    flag = True
    if origin == "":
        flag = False
        url1 = "http://mighty-cliffs-82717.herokuapp.com/api/posts/" + parent_id + "/comments/"
    else:
        url1 = origin + "/comments/"

    # this works for posting a comment to ourselves
    #url1 = "http://" + request.get_host() + "/api/posts/" + parent_id + "/comments/"#?id=" + str(author_object.id)

    req = urllib2.Request(url1)
    req.add_header('Content-Type', 'application/json')
    if flag:
        base64string = base64.encodestring('%s:%s' % ("admin", "pass")).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string) 


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

    post_id = uuid.uuid4()
    DITTO_HOST = 'http://' + request.get_host() + '/api/posts/' + str(post_id)
    title = request.POST.get('title')
    description = request.POST.get('description')

    categories = request.POST.get('categories')

    c = categories.split(' ')

    categories_json = json.dumps(c)

    new_post = Post(published=published, author=author_object, content=content, contentType=contentType,
                    visibility=visibility, source=DITTO_HOST, origin=DITTO_HOST, categories=categories, title=title,
                    description=description, id = post_id)
    new_post.save()

    return HttpResponse(request.POST.get('post_body'))
