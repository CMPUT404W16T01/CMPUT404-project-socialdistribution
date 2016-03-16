from rest_framework import serializers
from feed.models import Post, Comment, Author


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description', 'is_markdown', 'body', 'author_id', 'categories',
            'date_published', 'post_id', 'visibility')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'date_published', 'author_id')

class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Author
		fields = (
			'user_id', 'host', 'display_name', 'github_account', 'email', 'bio')

