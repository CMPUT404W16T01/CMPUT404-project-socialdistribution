import json

from django.http import Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PostSerializer, CommentSerializer, AuthorSerializer, AllAuthorSerializer
from feed.models import Post, Author, Comment, Friend, CommentAuthor

import requests


class public_posts(APIView):
    """
    List all posts.
    """

    def get(self, request, format=None):
        posts = Post.objects.filter(visibility="PUBLIC")
        serializer = PostSerializer(posts, many=True)
        return Response({"query": "posts", "count": len(posts), "size": "", "next": "",
                         "previous": "http://previouspageurlhere", "posts": serializer.data})


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
        post_object = Post.objects.get(id=pk)
        comments = Comment.objects.filter(id=post_object)
        serializer = CommentSerializer(comments, many=True)
        return Response({"query": "comments", "count": len(comments), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "comments": serializer.data})

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


class author_posts(APIView):
    """
    List all posts.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        author_object = Author.objects.get(id=pk)
        asker_id = request.GET.get('id')

        public_posts = Post.objects.filter(author=author_object, visibility="PUBLIC")
        return_posts = public_posts

        if (pk == asker_id):
        	private_posts = Posts.objects.filter(author=author_object, visibility="PRIVATE")
        	return_posts = return_posts | private_posts

        # if the asker is on our server, need to check if they are on our server first
        if (len(Author.objects.filter(id=asker_id)) > 0):
        	server_only_posts = Posts.objects.filter(author=author_object, visibility="SERVERONLY")
        	return_posts = return_posts | server_only_posts

        # if the asker is a friend
        friend_to_author = Friend.objects.filter(follower_id=pk, followed_id=asker_id)
        author_to_friend = Friend.objects.filter(follower_id=asker_id, followed_id=pk)
        if (len(friend_to_author) == 1) and (len(author_to_friend) == 1):
        	#then they are friends, because the relationship is mutual
        	friend_posts = Posts.objects.filter(author=author_object, visibility="FRIENDS")
        	return_posts = return_posts | server_only_posts

        # TODO: Look at FOAF stuff

        serializer = PostSerializer(return_posts, many=True)
        return Response({"query": "posts", "count": len(posts), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "posts": serializer.data})


class author_comments(APIView):
    """
    List all comments from a specific author
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        author_object = Author.objects.get(id=pk)
        comments = Comment.objects.filter(author=author_object)
        serializer = CommentSerializer(comments, many=True)
        return Response({"query": "comments", "count": len(comments), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "comments": serializer.data})


class author_list(APIView):
    """
    List all authors
    """

    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

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
        return Response({"query": "author", "count": "1", "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "author": serializer.data})


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
        #print len(friend_to_author)

        # am I followign them
        #print len(author_to_friend)

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
            # TODO: SEND SOMETHING TO THE FRIENDS PAGE TO ALERT FRIEND REQUEST

        # CHECK THE USERS, IF ONE OF THEM IS OFF SERVER WE MUST POST TO THEIR SERVER
        # this gets called even when we don't need to send them requests
        if ("mighty-cliffs-82717" in author_host) or ("mighty-cliffs-82717" in friend_host):
            try:
                #url = 'http://' + 'localhost:8001' + '/api/friendrequest'
                url = 'http://mighty-cliffs-82717.herokuapp.com/api/friendrequest'
                packet = {"query":"friendrequest", "author":author, "friend":friend }
                r = requests.post(url, json=packet)
                print "ahhh we sent something"
            except:
                pass


        return Response()
