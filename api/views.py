from feed.models import Post, Author, Comment
from api.serializers import PostSerializer, CommentSerializer, AuthorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
import json


class public_posts(APIView):
    """
    List all posts.
    """

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializerloads(posts, many=True)
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
        post_object = Post.objects.get(id=pk)
        comments = Comment.objects.filter(id=post_object)
        serializer = CommentSerializer(comments, many=True)
        return Response({"query": "comments", "count": len(comments), "size": "10", "next": "http://nextpageurlhere",
                         "previous": "http://previouspageurlhere", "comments": serializer.data})

    def post(self, request, pk, format=None):
        comment = request.data.get('comment')
        author_object = request.data.get('author')
        author_name = author_object['displayName']
        print "here"

        published = request.data.get('published')
        contentType = request.data.get('contentType')
        post_object = Post.objects.get(id=pk)
        print "zxcv"

        new_comment = Comment(author=json.dumps(author_object), post_id=post_object, 
            comment=comment,  published=published, 
            author_name=author_name, contentType=contentType)
        new_comment.save()



        return Response({})


class author_posts(APIView):
    """
    List all posts.
    """

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

    def get(self, request, pk, format=None):
        author_object = Author.objects.get(id=pk)
        serializer = AuthorSerializer(author_object)
        return Response({"query": "author", "count": "1", "size": "10", "next": "http://nextpageurlhere",
                 "previous": "http://previouspageurlhere", "author": serializer.data})
