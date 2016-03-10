from django.shortcuts import render
from serializers import PostSerializer
from feed.models import Post
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def public_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({"query":"posts", "count":len(posts), "size":"10", "next":"http://nextpageurlhere", "previous":"http://previouspageurlhere", "posts": serializer.data})