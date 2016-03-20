from feed.models import Post, Author, Comment, Friend
from api.serializers import PostSerializer, CommentSerializer, AuthorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json


class public_posts(APIView):
    """
    List all posts.
    """

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response({"query": "posts", "count": len(posts), "size": "10", "next": "http://nextpageurlhere",
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
        snippet = self.get_object(pk)
        serializer = PostSerializer(snippet)
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
        # print "here"

        published = request.data.get('published')
        contentType = request.data.get('contentType')
        post_object = Post.objects.get(id=pk)
        # print "zxcv"

        new_comment = Comment(author=json.dumps(author_object), post_id=post_object,
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
        posts = Post.objects.filter(author_id=author_object)
        serializer = PostSerializer(posts, many=True)
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
        comments = Comment.objects.filter(author_id=author_object)
        serializer = CommentSerializer(comments, many=True)
        return Response({"query": "comments", "count": len(comments), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "comments": serializer.data})


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
        print request.data
        author = json.loads(request.data.get("author"))
        friend = json.loads(request.data.get("friend"))
        author_host = author.get("host")
        friend_host = friend.get("host")
        friend_to_author = Friend.objects.filter(follower_id=friend["id"], followed_id=author["id"])
        author_to_friend = Friend.objects.filter(follower_id=author["id"], followed_id=friend["id"])
        # checks what kind of relationship the two have, intimate or otherwise
        if (len(friend_to_author) > 0) and (len(author_to_friend) > 0):
            print "you're an idiot you're already friends"
        elif (len(friend_to_author) > 0):
            print "asdf"
            new_friend_object = Friend(follower_id=friend["id"], followed_id=author["id"],
                                       follower_host=friend_host, followed_host=author_host)
            new_friend_object.save()
            # WE ARE NOW FRIENDS
        else:
            print "we hit here"
            new_friend_object = Friend(follower_id=author["id"], followed_id=friend["id"],
                                       follower_host=author_host, followed_host=friend_host)
            new_friend_object.save()
            # TODO: SEND SOMETHING TO THE FRIENDS PAGE TO ALERT FRIEND REQUEST

        return Response()
