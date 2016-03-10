from feed.models import Post
from api.serializers import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
