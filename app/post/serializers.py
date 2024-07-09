"""
Serializers for the api end points of the post
"""

from rest_framework import serializers

from core.models import Post, Tag, PostServiceEvents
from services import serializers as servicesSerializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class PostSerializer(serializers.ModelSerializer):
    """Serializers for the post object."""
    tags = TagSerializer(many=True, required=False)
    service_requested = servicesSerializers.PostServiceEventsSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'description',
                  'link', 'tags', 'service_requested', 'status', 'image']
        read_only_fields = ['id']

    def _get_or_create_tag(self, tags, post):
        """Get or create a tag."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(user=auth_user, **tag)
            post.tags.add(tag)

    def _get_or_create_service_requested(self, service_requested, post):
        """Get or create a service requested."""
        auth_user = self.context['request'].user
        for service_data in service_requested:
            service_event, created = PostServiceEvents.objects.get_or_create(
                post=post,
                user=auth_user,
                # Assuming service_data is a dict
                # with the fields for PostServiceEvents
                defaults=service_data
            )
            if not created:
                # Update the service_event with new data if it already existed
                for key, value in service_data.items():
                    setattr(service_event, key, value)
                service_event.save()

    # This is overriding there create method to create a new post object
    def create(self, validated_data):
        """Create a new post and return it."""
        # NOTE: this is the default implementation
        # return Post.objects.create(**validated_data)
        """Create a new post and return it."""
        tags = validated_data.pop('tags', [])
        print('validated_data', validated_data)
        service_requested = validated_data.pop('service_requested', [])
        post = Post.objects.create(**validated_data)
        self._get_or_create_tag(tags, post)
        print('service_requested', service_requested)
        self._get_or_create_service_requested(service_requested, post)

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
