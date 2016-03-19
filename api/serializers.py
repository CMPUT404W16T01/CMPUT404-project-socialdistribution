from rest_framework import serializers
from feed.models import Post, Comment, Author


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description', 'contentType', 'content', 'author_id', 'categories',
            'published', 'id', 'visibility')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'published', 'author_id')


class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Author
		fields = (
			'id', 'host', 'displayName', 'github', 'email', 'bio')

class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id', 'host', 'displayName', 'github', 'bio')
