import json
import requests
import urllib2
import base64


from django.http import Http404
from django.core.paginator import Paginator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.serializers import PostSerializer, CommentSerializer, AuthorSerializer, AllAuthorSerializer
from feed.models import Post, Author, Comment, Friend, CommentAuthor, ForeignHost

DEFAULT_PAGE_NUM = 0
DEFAULT_PAGE_SIZE = 10


class public_posts(APIView):
    """
    List all posts.
    """

    def get(self, request, format=None):

        page_num = int(request.GET.get('page', DEFAULT_PAGE_NUM))
        page_size = int(request.GET.get('size', DEFAULT_PAGE_SIZE))

        posts = Post.objects.filter(visibility="PUBLIC")
        pages = Paginator(posts, page_size)
        page = pages.page(page_num+1)
        page_data = page.object_list
        serializer = PostSerializer(page_data, many=True)

        response = {"query": "posts", "count": len(posts), "size": page_size, "posts": serializer.data}

        if page.has_next():
            response['next'] = 'http://ditto-test.herokuapp.com/api/posts/?page=' + str(page_num + 1) + '&size=' + str(page_size)
        if page.has_previous():
            response['previous'] = 'http://ditto-test.herokuapp.com/api/posts/?page=' + str(page_num -1) + '&size=' + str(page_size)

        return Response(response)


class post_detail(APIView):
    """
    Retrieve a single post.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class post_comments(APIView):
    """
    List all comments for a single post.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):

        page_num = int(request.GET.get('page', DEFAULT_PAGE_NUM))
        page_size = int(request.GET.get('size', DEFAULT_PAGE_SIZE))

        post_object = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post_id=post_object)
        pages = Paginator(comments, page_size)
        page = pages.page(page_num+1)
        page_data = page.object_list
        serializer = CommentSerializer(page_data, many=True)
        response = {"query": "comments", "count": len(comments), "size": page_size, "comments": serializer.data}

        if page.has_next():
            response['next'] = 'http://ditto-test.herokuapp.com/api/posts/' + pk + '/comments/?page=' + str(page_num + 1) + '&size=' + str(page_size)
        if page.has_previous():
            response['previous'] = 'http://ditto-test.herokuapp.com/api/posts/' + pk + '/comments/?page=' + str(page_num - 1) + '&size=' + str(page_size)

        return Response(response)

    def post(self, request, pk, format=None):
        comment = request.data.get('comment')
        author_object = request.data.get('author')
        author_name = author_object['displayName']

        published = request.data.get('published')
        contentType = request.data.get('contentType')
        post_object = Post.objects.get(id=pk)
        new_comment_author = CommentAuthor(id=author_object['id'], host=author_object['host'], displayName=author_name,
                                           url=author_object['url'], github=author_object['github'])
        new_comment_author.save()
        new_comment = Comment(author=new_comment_author, post_id=post_object,
                              comment=comment, published=published,
                              author_name=author_name, contentType=contentType)
        new_comment.save()

        return Response({})


class all_auth_posts(APIView):
    """
    List all posts that the current asking author can see, hosted on our server
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        page_num = int(request.GET.get('page', DEFAULT_PAGE_NUM))
        page_size = int(request.GET.get('size', DEFAULT_PAGE_SIZE))

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
                all_posts = Post.objects.filter(author=asker_object)
                return_posts = return_posts | all_posts
                continue

            # if the asker is a friend
            friend_to_author = Friend.objects.filter(follower_id=each_id, followed_id=asker_id)
            author_to_friend = Friend.objects.filter(follower_id=asker_id, followed_id=each_id)

            if (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
                # then they are friends, because the relationship is mutual
                friend_posts = Post.objects.filter(author=each, visibility="FRIENDS")
                return_posts = return_posts | friend_posts

            # if the asker is on our server, and a friend
            if (len(Author.objects.filter(id=asker_id)) > 0) and (len(friend_to_author) == 1) and (
                len(author_to_friend) == 1):
                server_friends_posts = Post.objects.filter(author=each, visibility="SERVERONLY")
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
                if ((len(friend_to_author) == 1) and (len(author_to_friend) == 1)) or (each_id == asker_id):
                    foaf_posts = Post.objects.filter(author=each, visibility="FOAF")
                    return_posts = return_posts | foaf_posts
                    break
                else:
                    # we should check if we are friends of any of A's friends
                    # author is a string of a uuid
                    a_to_b = Friend.objects.filter(follower_id=asker_id, followed_id=author)
                    b_to_a = Friend.objects.filter(follower_id=author, followed_id=asker_id)
                    if (len(a_to_b) == 1) and (len(b_to_a) == 1):
                        # we are friends with one of their friends
                        foaf_posts = Post.objects.filter(author=each, visibility="FOAF")
                        return_posts = return_posts | foaf_posts
                        break

        pages = Paginator(return_posts, page_size)
        page = pages.page(page_num + 1)
        page_data = page.object_list
        serializer = PostSerializer(page_data, many=True)

        response = {"query": "posts", "count": len(return_posts), "size": page_size, "posts": serializer.data}

        if page.has_next():
            response['next'] = 'http://ditto-test.herokuapp.com/api/posts/?page=' + str(page_num + 1) + '&size=' + str(page_size)
        if page.has_previous():
            response['previous'] = 'http://ditto-test.herokuapp.com/api/posts/?page=' + str(page_num - 1) + '&size=' + str(page_size)

        return Response(response)


class author_posts(APIView):
    """
    List all posts of an author that can be seen by the authenticated user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        page_num = int(request.GET.get('page', DEFAULT_PAGE_NUM))
        page_size = int(request.GET.get('size', DEFAULT_PAGE_SIZE))

        author_object = Author.objects.get(id=pk)

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
        if pk == asker_id:
            all_posts = Post.objects.filter(author=author_object)

            pages = Paginator(all_posts, page_size)
            page = pages.page(page_num + 1)
            page_data = page.object_list
            serializer = PostSerializer(page_data, many=True)

            response = {"query": "posts", "count": len(return_posts), "size": page_size, "posts": serializer.data}

            if page.has_next():
                response['next'] = 'http://ditto-test.herok.com/api/posts/?page=' + str(page_num + 1) + '&size=' + str(page_size)
            if page.has_previous():
                response['previous'] = 'http://ditto-test.herokuapp.com/api/posts/?page=' + str(page_num - 1) + '&size=' + str(
                    page_size)

            return Response(response)

            # if the asker is a friend
        friend_to_author = Friend.objects.filter(follower_id=pk, followed_id=asker_id)
        author_to_friend = Friend.objects.filter(follower_id=asker_id, followed_id=pk)

        if (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
            # then they are friends, because the relationship is mutual
            friend_posts = Post.objects.filter(author=author_object, visibility="FRIENDS")
            return_posts = return_posts | friend_posts

        # if the asker is on our server, and a friend
        if (len(Author.objects.filter(id=asker_id)) > 0) and (len(friend_to_author) == 1) and (
            len(author_to_friend) == 1):
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
            if ((len(friend_to_author) == 1) and (len(author_to_friend) == 1)) or (pk == asker_id):
                foaf_posts = Post.objects.filter(author=author_object, visibility="FOAF")
                return_posts = return_posts | foaf_posts
                break
            else:
                # we should check if we are friends of any of A's friends
                # author is a string of a uuid
                a_to_b = Friend.objects.filter(follower_id=pk, followed_id=author)
                b_to_a = Friend.objects.filter(follower_id=author, followed_id=pk)
                if (len(a_to_b) == 1) and (len(b_to_a) == 1):
                    # we are friends with one of their friends
                    foaf_posts = Post.objects.filter(author=author_object, visibility="FOAF")
                    return_posts = return_posts | foaf_posts
                    break

        pages = Paginator(return_posts, page_size)
        page = pages.page(page_num + 1)
        page_data = page.object_list
        serializer = PostSerializer(page_data, many=True)

        response = {"query": "posts", "count": len(return_posts), "size": page_size, "posts": serializer.data}

        if page.has_next():
            response['next'] = 'http://ditto-test.herok.com/api/posts/?page=' + str(page_num + 1) + '&size=' + str(page_size)
        if page.has_previous():
            response['previous'] = 'http://ditto-test.herokuapp.com/api/posts/?page=' + str(page_num - 1) + '&size=' + str(
                page_size)

        return Response(response)   


class author_comments(APIView):
    """
    List all comments from a specific author
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        page_num = int(request.GET.get('page', DEFAULT_PAGE_NUM))
        page_size = int(request.GET.get('size', DEFAULT_PAGE_SIZE))

        author_object = Author.objects.get(id=pk)
        comments = Comment.objects.filter(author=author_object)
        pages = Paginator(comments, page_size)
        page = pages.page(page_num + 1)
        page_data = page.object_list
        serializer = CommentSerializer(page_data, many=True)

        response = {"query": "comments", "count": len(comments), "size": page_size, "comments": serializer.data}

        if page.has_next():
            response['next'] = 'http://ditto-test.herokuapp.com/api/posts/' + pk + '/comments/?page=' + str(
                page_num + 1) + '&size=' + str(page_size)
        if page.has_previous():
            response['previous'] = 'http://ditto-test.herokuapp.com/api/posts/' + pk + '/comments/?page=' + str(
                page_num - 1) + '&size=' + str(page_size)

        return Response(response)


class author_list(APIView):
    """
    List all authors
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        authors = Author.objects.filter(admin_auth=True)
        serializer = AllAuthorSerializer(authors, many=True)
        return Response({"authors": serializer.data})


class author_detail(APIView):
    """
    List all information on provided author
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        author_object = Author.objects.get(id=pk)
        serializer = AuthorSerializer(author_object)
        response = serializer.data
        response['friends'] = []

        following = Friend.objects.filter(follower_id=pk)

        for i in following:
            tmp = Friend.objects.filter(follower_id=i.followed_id, followed_id=i.follower_id)
            if len(tmp) > 0:
                response['friends'].append(i.followed_id)
        return Response(response)


class check_friends(APIView):
    """
    returns who are friends
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    # returns 
    def get(self, request, pk, format=None):
        author_id = pk
        friends = []

        following = Friend.objects.filter(follower_id=author_id)

        for i in following:
            tmp = Friend.objects.filter(follower_id=i.followed_id, followed_id=i.follower_id)
            if len(tmp) > 0:
                friends.append(i.followed_id)

        packet = {"query": "friends",
                  "authors": friends}

        return Response(packet)

    def post(self, request, pk, format=None):
        author_id = pk
        possible_friends = request.data.get('authors')
        confirmed_friends = []

        for author_id in possible_friends:
            author_one_to_two = Friend.objects.filter(follower_id=pk, followed_id=author_id)
            author_two_to_one = Friend.objects.filter(follower_id=author_id, followed_id=pk)
            if (len(author_one_to_two) > 0) and (len(author_two_to_one) > 0):
                confirmed_friends.append(author_id)

        packet = {"query": "friends",
                  "author": pk,
                  "authors": confirmed_friends}

        return Response(packet)


class check_mutual_friend(APIView):
    """
    Return JSON with True or False if friends
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk1, pk2, format=None):
        author_one_to_two = Friend.objects.filter(follower_id=pk1, followed_id=pk2)
        author_two_to_one = Friend.objects.filter(follower_id=pk2, followed_id=pk1)

        packet = {"query": "friends",
                  "authors": [pk1, pk2],
                  "friends": False}

        if (len(author_one_to_two) > 0) and (len(author_two_to_one) > 0):
            packet["friends"] = True

        return Response(packet)


class friend_request(APIView):
    """
    Make a friend (follow) request, if we have already followed the person who is requesting
    to become friends with us, they are actually responding to our friend request

    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            author = json.loads(request.data.get("author"))
            friend = json.loads(request.data.get("friend"))
        except:
            author = request.data.get("author")
            friend = request.data.get("friend")

        author_host = author.get("host")
        friend_host = friend.get("host")
        friend_to_author = Friend.objects.filter(follower_id=friend["id"], followed_id=author["id"])
        author_to_friend = Friend.objects.filter(follower_id=author["id"], followed_id=friend["id"])
        # checks what kind of relationship the two have, intimate or otherwise

        # are they following me?
        # print len(friend_to_author)

        # am I followign them
        # print len(author_to_friend)

        if (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
            print "you're an idiot you're already friends"

        elif (len(friend_to_author) == 1) and (len(author_to_friend) == 0):
            new_friend_object = Friend(follower_id=author["id"], followed_id=friend["id"],
                                       follower_host=author_host, followed_host=friend_host)
            new_friend_object.save()
            # WE ARE NOW FRIENDS

        elif (len(friend_to_author) == 0) and (len(author_to_friend) == 1):
            pass

        elif (len(friend_to_author) == 0) and (len(author_to_friend) == 0):
            new_friend_object = Friend(follower_id=author["id"], followed_id=friend["id"], follower_host=author_host,
                                       followed_host=friend_host)
            new_friend_object.save()

        # CHECK THE USERS, IF FRIEND IS NOT OUR SERVER, WE ARE SENDING A REQUEST OFF SERVER
        if 'ditto-test' not in friend_host:
            try:
                if "project" in friend_host:
                    friend_host = "http://project-c404.rhcloud.com/"
                url = friend_host + 'api/friendrequest'
                packet = {"query": "friendrequest", "author": author, "friend": friend}
                foreign_host = ForeignHost.objects.get(url=friend_host)
                r = requests.post(url, json=packet, auth=(foreign_host.username, foreign_host.password))
            except Exception as e:
                print e
                pass

        return Response()


class unfriend(APIView):
    """
    Unfriend people here
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # get friend object where followed_id = the person we're unfriending.
        author = request.data.get("author")
        unfriend_id = request.data.get("unfriending")
        print author, unfriend_id
        try:
            friend = Friend.objects.get(follower_id=str(author), followed_id=str(unfriend_id))
            # print friend.follower_id, friend.followed_id
            friend.delete()
        except e:
            print e

        return Response()
