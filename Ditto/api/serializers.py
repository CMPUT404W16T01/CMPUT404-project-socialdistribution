from rest_framework import serializers
from feed.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description', 'is_markdown', 'body', 'author_id', 'categories',
            'date_published', 'post_id', 'visibility')
