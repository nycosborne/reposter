"""
Serializers for the api end points of the post
"""

from rest_framework import serializers

from core.models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    """Serializers for the post object."""

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'description', 'link']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new post and return it."""
        return Post.objects.create(**validated_data)

    #
    # def update(self, instance, validated_data):
    #     """Update a post and return it."""
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.description = validated_data.get('description',
    #     instance.description)
    #     instance.link = validated_data.get('link', instance.link)
    #     instance.save()
    #     return instance


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail"""

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
