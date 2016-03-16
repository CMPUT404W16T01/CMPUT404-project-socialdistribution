from feed.models import Post, Author, Comment
from api.serializers import PostSerializer, CommentSerializer, AuthorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid


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

    def get(self, request, pk, format=None):
        post_object = Post.objects.get(post_id=pk)
        comments = Comment.objects.filter(post_id=post_object)
        serializer = CommentSerializer(comments, many=True)
        return Response({"query": "comments", "count": len(comments), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "comments": serializer.data})
        

class author_posts(APIView):
    """
    List all posts.
    """

    def get(self, request, pk, format=None):
        author_object = Author.objects.get(user_id=pk)
        posts = Post.objects.filter(author_id=author_object)
        serializer = PostSerializer(posts, many=True)
        return Response({"query": "posts", "count": len(posts), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "posts": serializer.data})

class author_comments(APIView):
    """
    List all comments from a specific author
    """

    def get(self, request, pk, format=None):
        author_object = Author.objects.get(user_id=pk)
        comments = Comment.objects.filter(author_id=author_object)
        serializer = CommentSerializer(comments, many=True)
        return Response({"query": "comments", "count": len(comments), "size": "10", "next": "http://nextpageurlhere",
                 "previous": "http://previouspageurlhere", "comments": serializer.data})


class author_detail(APIView):
    """
    List all information on provided author
    """

    def get(self, request, pk, format=None):
        author_object = Author.objects.get(user_id=pk)
        serializer = AuthorSerializer(author_object)
        return Response({"query": "author", "count": "1", "size": "10", "next": "http://nextpageurlhere",
                 "previous": "http://previouspageurlhere", "author": serializer.data})
