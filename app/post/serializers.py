"""
Serializers for the api end points of the post
"""

from rest_framework import serializers

from core.models import Post, Tag, SocialAccounts


class SocialAccountsSerializer(serializers.ModelSerializer):
    """Serializer for social accounts objects"""

    class Meta:
        model = SocialAccounts
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new social account and return it."""
        return SocialAccounts.objects.create(**validated_data)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class PostSerializer(serializers.ModelSerializer):
    """Serializers for the post object."""
    tags = TagSerializer(many=True, required=False)
    soc_accounts = SocialAccountsSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'description',
                  'link', 'tags', 'soc_accounts']
        read_only_fields = ['id']

    def _get_or_create_tag(self, tags, post):
        """Get or create a tag."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(user=auth_user, **tag)
            post.tags.add(tag)

    # This is overriding there create method to create a new post object
    def create(self, validated_data):
        """Create a new post and return it."""
        # NOTE: this is the default implementation
        # return Post.objects.create(**validated_data)
        """Create a new post and return it."""
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        self._get_or_create_tag(tags, post)

        return post

    def update(self, instance, validated_data):
        """Update a post and return it."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tag(tags, instance)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail"""

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['description', 'link', 'image']


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to posts"""

    class Meta:
        model = Post
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image': {'required': True}
        }
