from rest_framework import serializers
from feed.models import Post, Comment, Author


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'id', 'published')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url', 'github', 'email', 'bio')


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'github', 'bio')


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comments = serializers.SerializerMethodField('get_comments')

    def get_comments(self, obj):
        return CommentSerializer(Comment.objects.filter(post=obj.id), many=True).data

    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'comments' 'categories',
            'published', 'id', 'visibility')
