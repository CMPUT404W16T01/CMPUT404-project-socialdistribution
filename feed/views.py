from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from api.serializers import PostSerializer
from feed.models import Post, Git_Post, Author, Comment, ForeignHost, Friend, Img
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
import os
import uuid
import base64


# Create your views here.

@login_required
def feed(request):

    # calling http://ditto-test.herokuapp.com/api/author/posts?id=ASKING_USERS_ID
    # SHOULD just return all posts hosted by OUR server that the dude is supposed to see
    # so you can hopefully cut away all the manual parsing done here so far and do something like

    # url = http://ditto-test.herokuapp.com/api/author/posts?id=ASKING_USERS_ID
    # req = urllib2.Request(url)
    # base64string = base64.encodestring('%s:%s' % ("admin", "pass")).replace('\n', '')
    # req.add_header("Authorization", "Basic %s" % base64string)
    # response = urllib2.urlopen(req).read()
    # loaded = json.loads(response)
    # loaded['posts'] <- should be a list of all the posts
    # or try loaded.get('posts') 

    # assuming that happens, and that the other servers return the same thing all we have to do is call
    # this url once on every server and we are good to go, maybe parsing out duplicates

    user_object = User.objects.get(username=request.user.username)
    author_object = Author.objects.get(email=user_object)

    public_post_list = []
    their_post_list = []
    try:
        foreign_hosts = ForeignHost.objects.filter()
        their_post_list, public_post_list = getOurPosts(request, author_object)

        
        for i in foreign_hosts:
            url = i.url + "api/author/posts?id=" + str(author_object.id) #+ "&size=100"
            print url
            #url = i.url + "api/posts?size=100"
            req = urllib2.Request(url)

            base64string = base64.encodestring('%s:%s' % (i.username, i.password)).replace('\n', '')
            req.add_header("Authorization", "Basic %s" % base64string) 

            response = urllib2.urlopen(req).read()
            loaded = json.loads(response)

            their_posts = loaded.get('posts')
            print "beep"
            for post in their_posts:
                comments = []
                description = post.get("description")
                title = post.get("title")
                content = post.get("content")
                published_raw = post.get("published")
                origin = post.get("origin")
                id = post.get("id")
                visibility = post.get("visibility")
                published = datetime.strptime(published_raw, '%Y-%m-%dT%H:%M:%S.%fZ')
                published  = published.replace(tzinfo=None)

                their_comments = post.get("comments")
                if len(their_comments) > 0:
                    for comment1 in their_comments:
                        comment_body = comment1.get('comment')
          
                        comment_author = str(comment1.get('author').get('displayName'))

                        new_comment = Comment(author_name = comment_author, comment = comment_body)
                        comments.append(new_comment)
                new_post = Post( id = id, description = description, title = title, content = content, published = published, origin = origin, visibility = visibility)
                new_post.comments = comments
                new_post.magic_author = post.get("author").get("id")

                if post.get("visibility"):
                    public_post_list.append(new_post)
                their_post_list.append(new_post)
                # print "Main:" + en(their_post_list) + " Pub: " + len(public_post_list)

    except Exception as e:
        print e
        print "couldn't get other hosts posts"



    # user_object = User.objects.get(username=request.user.username)
    # author_object = Author.objects.get(email=user_object)

    github_name = "".join((author_object.github).split())




    public_posts = public_post_list
    for x in public_posts:
      x.published= x.published.replace(tzinfo=None)
    public_posts.sort(key=lambda x: x.published, reverse=True)

    # # My feed, access all posts that I can see
    self_posts = Post.objects.filter(author_id=author_object)
    all_comments = Comment.objects.all()


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

    for x in self_posts_list:
        x.published= x.published.replace(tzinfo=None)
    self_posts_list.sort(key=lambda x: x.published, reverse=True)

    # end of self feed

    # start of github feed
    github_posts = create_github_post(github_name)
    # end of github feed

    main_posts = their_post_list

    return_main_posts = []
    friends = Friend.objects.filter(follower_id=author_object.id)
    friends_list = []
    for friend in friends:
        friends_list.append(str(friend.followed_id))

    for post in main_posts:
        if str(author_object.id) == str(post.magic_author):
            return_main_posts.append(post)
        elif str(post.magic_author) in friends_list:
            return_main_posts.append(post)



    for x in return_main_posts:
      x.published= x.published.replace(tzinfo=None)
    return_main_posts.sort(key=lambda x: x.published, reverse=True)

    
    context = {
        'main_posts': return_main_posts,
        'public_posts': public_posts,
        'my_posts': self_posts_list,
        "github_posts": github_posts,
    }

    return render(request, 'feed.html', context)

def getOurPosts(request, author_object):
    asker_host = request.META.get("HTTP_HOST")
    try:
        asker_object = Author.objects.get(email=request.user)
        asker_id = str(asker_object.id)
    except:
        asker_id = request.GET.get('id', default=None)
        asker_id = asker_id.strip("/")
        if asker_id == None:
            return Response({"details": "give and ?id=xxxx"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            asker_id = str(asker_id)



    public_posts = Post.objects.filter(visibility="PUBLIC")
    return_posts = public_posts


    all_authors = Author.objects.filter()

    for each in all_authors:
        each_id = str(each.id)

        # the asker is the user itself, add in what only they could see
        if (each_id == asker_id):
            own_posts = Post.objects.filter(author=asker_object)
            return_posts = return_posts | own_posts
            continue
      
        # if the asker is a friend
        friend_to_author = Friend.objects.filter(follower_id=each_id, followed_id=asker_id)
        author_to_friend = Friend.objects.filter(follower_id=asker_id, followed_id=each_id)

        if (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
            #then they are friends, because the relationship is mutual
            friend_posts = Post.objects.filter(author=each, visibility="FRIENDS")
            return_posts = return_posts | friend_posts

        # if the asker is on our server, and a friend
        if (len(Author.objects.filter(id=asker_id)) > 0) and (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
            server_friends_posts = Post.objects.filter(author=each, visibility="SERVERONLY")
            return_posts = return_posts | server_friends_posts

        # asker_id is person A
        # as ditto, we need to ask person A's host who A is friends with

        # fetch list of A's friends
        url = "http://" + asker_host + "/api/friends/" + asker_id + "?size=100"
        req = urllib2.Request(url)


        # assume we are sending to ourselves to begin with, if we are getting this from
        # another host then we will update after
        base64string = base64.encodestring('%s:%s' % ("admin", "pass")).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)

        foreign_hosts = ForeignHost.objects.filter()
        for host in foreign_hosts:
            # if the sender host, which is a clipped version of the full host path, is part of it, then that host
            # is the correct one we're looking for
            if asker_host in host.url:
                base64string = base64.encodestring('%s:%s' % (host.username, host.password)).replace('\n', '')
                req.add_header("Authorization", "Basic %s" % base64string)


        response = urllib2.urlopen(req).read()
        loaded = json.loads(response)


        # we now have a list of authors who are friends with the asker
        # if we are friends with any of them then we can give them our FOAF marked posts
        # or if we were friends to begin with they can also see FOAF marked posts

        for author in loaded['authors']:
            # if we are directly friends lets just give it to them
            if ((len(friend_to_author) == 1) and (len(author_to_friend) == 1)) or (each_id == asker_id):
                foaf_posts = Post.objects.filter(author=each, visibility="FOAF")
                return_posts = return_posts | foaf_posts
                break
            else:
                # we should check if we are friends of any of A's friends
                #author is a string of a uuid
                a_to_b = Friend.objects.filter(follower_id=asker_id, followed_id=author)
                b_to_a = Friend.objects.filter(follower_id=author, followed_id=asker_id)
                if (len(a_to_b) == 1) and (len(b_to_a) == 1):
                    # we are friends with one of their friends
                    foaf_posts = Post.objects.filter(author=each, visibility="FOAF")
                    return_posts = return_posts | foaf_posts
                    break


    response = PostSerializer(return_posts, many=True)
    beep = {"query": "posts", "count": len(return_posts), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "posts": response.data}

    boop = json.dumps(beep)
    loaded = json.loads(boop)


    our_posts = loaded.get('posts')

    return_public_posts = []
    return_main_posts = []

    for post in our_posts:
        comments = []
        description = post.get("description")
        title = post.get("title")
        content = post.get("content")
        published_raw = post.get("published")
        origin = post.get("origin")
        id = post.get("id")
        visibility = post.get("visibility")

        published = datetime.strptime(published_raw, '%Y-%m-%dT%H:%M:%S.%fZ')
        published  = published.replace(tzinfo=None)

        their_comments = post.get("comments")
        if len(their_comments) > 0:
            for comment1 in their_comments:
                comment_body = comment1.get('comment')

                comment_author = str(comment1.get('author').get('displayName'))

                new_comment = Comment(author_name = comment_author, comment = comment_body)
                comments.append(new_comment)
        new_post = Post( id = id, description = description, title = title, content = content, published = published, origin = origin, visibility = visibility)
        new_post.comments = comments
        new_post.magic_author = post.get("author").get("id")


        if (str(author_object.id) == str(post.get('author').get('id'))):
            new_post.flag = True
        else:
            new_post.flag = False


        if post.get("visibility") == "PUBLIC":
            return_public_posts.append(new_post)
        return_main_posts.append(new_post)





    return return_main_posts, return_public_posts
  


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
            foreign_hosts = ForeignHost.objects.filter()
            for i in foreign_hosts:
                if 'project' in i.url:
                    url = i.url + "/api/author"
                else:
                    url = i.url + "/api/authors"
                r = requests.get(url, auth=(i.username, i.password))

                foreign_authors = json.loads(r.text)

                if 'project' in i.url:
                    for each in foreign_authors:
                        if each['id'] == pk:
                            them_object = each
                            them_id = them_object.get('id')
                            them_host = them_object.get('host')
                            break 
                else:
                    for each in foreign_authors['authors']:
                        if each['id'] == pk:
                            them_object = each
                            them_id = them_object.get('id')
                            them_host = them_object.get('host')
                            break

            # get the posts from that user
            print them_host
            if 'project' in them_host:
                them_host = "http://project-c404.rhcloud.com/"

            foreign_host = ForeignHost.objects.get(url=them_host)
            url = them_host + "api/author/" + them_id + "/posts?id=" + str(us_object.id)
            print url
            req = urllib2.Request(url)

            base64string = base64.encodestring('%s:%s' % (foreign_host.username, foreign_host.password)).replace('\n', '')
            req.add_header("Authorization", "Basic %s" % base64string)

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

            return_posts = their_post_list
            for x in return_posts:
                x.published= x.published.replace(tzinfo=None)
            return_posts.sort(key=lambda x: x.published, reverse=True)


            context = {
                "sender": us_object,
                "them": them_object,
                "main_posts": return_posts
            }

        except Exception as e:
            print e
            # do something maybe
            context = {
                "sender": us_object,
                "them": them_object,
                "main_posts": []
            }
    else:
        them_object = them_object[0]
        them_id = str(them_object.id)
        them_host = them_object.host

        try:
            author_object = Author.objects.get(id=pk)
        except: 
            print "Author is offhost and is causing errors later in this code"

        asker_host = request.META.get("HTTP_HOST")

        try:
            asker_object = Author.objects.get(email=request.user)
            asker_id = str(asker_object.id)
        except:
            asker_id = request.GET.get('id', default=None)
            if asker_id == None:
                return Response({"details": "give and ?id=xxxx"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                asker_id = str(asker_id)


        public_posts = Post.objects.filter(author=author_object, visibility="PUBLIC")
        return_posts = public_posts

        # the asker is the user itself, return everything
        if (pk == asker_id):
            all_posts = Post.objects.filter(author=author_object)
            return_posts = all_posts

            for a in return_posts:
                current_post_id = a.id
                comments_list = Comment.objects.filter(post_id=current_post_id)
                posts_comments = []
                for com in comments_list:
                    comment_body = com.comment
                    comment_author = com.author_name
                    new_comment = Comment(author_name=comment_author, comment=comment_body)
                    posts_comments.append(new_comment)
                a.comments = posts_comments

            context = {
                'sender': us_object,
                'them': them_object,
                'main_posts': return_posts,
            }

            return render(request, 'profile.html', context)

          
        # if the asker is a friend
        friend_to_author = Friend.objects.filter(follower_id=pk, followed_id=asker_id)
        author_to_friend = Friend.objects.filter(follower_id=asker_id, followed_id=pk)

        if (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
            #then they are friends, because the relationship is mutual
            friend_posts = Post.objects.filter(author=author_object, visibility="FRIENDS")
            return_posts = return_posts | friend_posts

        # if the asker is on our server, and a friend
        if (len(Author.objects.filter(id=asker_id)) > 0) and (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
            server_friends_posts = Post.objects.filter(author=author_object, visibility="SERVERONLY")
            return_posts = return_posts | server_friends_posts

        # TODO: Look at FOAF stuff
        # asker_id is person A
        # as ditto, we need to ask person A's host who A is friends with

        # fetch list of A's friends
        url = "http://" + asker_host + "/api/friends/" + asker_id
             
        req = urllib2.Request(url)

        # assume we are sending to ourselves to begin with, if we are getting this from
        # another host then we will update after
        base64string = base64.encodestring('%s:%s' % ("admin", "pass")).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)


        foreign_hosts = ForeignHost.objects.filter()
        for host in foreign_hosts:
            # if the sender host, which is a clipped version of the full host path, is part of it, then that host
            # is the correct one we're looking for
            if asker_host in host.url:
                base64string = base64.encodestring('%s:%s' % (host.username, host.password)).replace('\n', '')
                req.add_header("Authorization", "Basic %s" % base64string)

        response = urllib2.urlopen(req).read()
        loaded = json.loads(response)


        # we now have a list of authors who are friends with the asker
        # if we are friends with any of them then we can give them our FOAF marked posts
        # or if we were friends to begin with they can also see FOAF marked posts

        for author in loaded['authors']:
            # if we are directly friends lets just give it to them
            if (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
                foaf_posts = Post.objects.filter(author=author_object, visibility="FOAF")
                return_posts = return_posts | foaf_posts
                break
            else:
                # we should check if we are friends of any of A's friends
                #author is a string of a uuid
                a_to_b = Friend.objects.filter(follower_id=pk, followed_id=author)
                b_to_a = Friend.objects.filter(follower_id=author, followed_id=pk)
                if (len(a_to_b) == 1) and (len(b_to_a) == 1):
                    # we are friends with one of their friends
                    foaf_posts = Post.objects.filter(author=author_object, visibility="FOAF")
                    return_posts = return_posts | foaf_posts
                    break

        for a in return_posts:
            current_post_id = a.id
            comments_list = Comment.objects.filter(post_id=current_post_id)
            posts_comments = []
            for com in comments_list:
                comment_body = com.comment
                comment_author = com.author_name
                new_comment = Comment(author_name=comment_author, comment=comment_body)
                posts_comments.append(new_comment)
                print comment_body
            a.comments = posts_comments

        context = {
            'sender': us_object,
            'them': them_object,
            'main_posts': return_posts,
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
    # if "origin":"http://whereitcamefrom.com/api/posts/zzzzz", 

    # url1 = origin + "/comments/"

    # janky stuff, we should just fix our api for the url

    if 'ditto-test' in origin:
        url1 = origin + "/comments/"
    elif 'mighty' not in origin:
        url1 = "http://project-c404.rhcloud.com/api/posts/" + parent_id + "/comments/" 
    else:
        url1 = origin + "/comments/" # + "/api/posts/" + parent_id + "/comments"

    print url1
    print json_packet
    # this works for posting a comment to ourselves
    #url1 = "http://" + request.get_host() + "/api/posts/" + parent_id + "/comments/"


    req = urllib2.Request(url1)
    req.add_header('Content-Type', 'application/json')
    foreign_hosts = ForeignHost.objects.filter()

    if 'ditto-test' in origin:
        base64string = base64.encodestring('%s:%s' % ("admin", "pass")).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)
    else:
        for host in foreign_hosts:
            if host.url in origin:
                base64string = base64.encodestring('%s:%s' % (host.username, host.password)).replace('\n', '')
                req.add_header("Authorization", "Basic %s" % base64string) 

    urllib2.urlopen(req, json_packet)
    # new_comment.save()
    return redirect('/feed')



def create_post(request):
    print request.FILES.get('file')
    print type(request.FILES.get('file'))
    image = request.FILES.get('file')

    content = request.POST.get('post-input')
    published = datetime.now()
    is_markdown = json.loads(request.POST.get('is-markdown-post'))
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
    if image:
        print image.content_type
        #image.name = str(uuid.uuid4())
        print image.name
        print "before creating"
        new_image = Img(actual_image = image)
        new_image.parent_post = new_post

        print "before saving"
        new_image.save()
        print "after saving"

        new_post.content = new_post.content + ' <br>   <img src="http://ditto-test.herokuapp.com/ditto/media/images/'+image.name+'" >'
        #new_post.content = new_post.content + ' <br>   <img src="http://localhost:8000/ditto/media/images/'+image.name+'" >'
        new_post.save()

    return HttpResponse(request.POST.get('post_body'))
