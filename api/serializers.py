from rest_framework import serializers
from feed.models import Post, Comment, Author, CommentAuthor, Friend


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentAuthor
        fields = ('id', 'host', 'displayName', 'url', 'github')


class CommentSerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer()

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'id', 'published')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url', 'github', 'bio')


class AllAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url')


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField('get_post_comments')

    def get_post_comments(self, obj):
        return CommentSerializer(Comment.objects.filter(post_id=obj.id), many=True).data

    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'comments',
            'categories', 'published', 'id', 'visibility')
