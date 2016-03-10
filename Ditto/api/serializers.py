from rest_framework import serializers
from feed.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'published', 'id', 'visibility')