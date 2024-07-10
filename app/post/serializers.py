"""
Serializers for the api end points of the post
"""

from rest_framework import serializers

from core.models import Post, Tag, PostServiceEvents
from services import serializers as servicesSerializers

from services.serializers import PostServiceEventsSerializer


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class PostSerializer(serializers.ModelSerializer):
    """Serializers for the post object."""
    tags = TagSerializer(many=True, required=False)
    post_service_events = servicesSerializers.PostServiceEventsSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'description',
                  'link', 'tags', 'post_service_events', 'status', 'image']
        read_only_fields = ['id']

    def _get_or_create_tag(self, tags, post):
        """Get or create a tag."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(user=auth_user, **tag)
            post.tags.add(tag)

    def _get_or_create_service_requested(self, service_requested, post):
        """Get or create service requested."""
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
            else:
                # Create a new service event
                service_event = PostServiceEvents.objects.create(
                    post=post, user=auth_user, **service_data
                )

    # This is overriding there create method to create a new post object
    def create(self, validated_data):
        """Create a new post and return it."""
        # NOTE: this is the default implementation
        # return Post.objects.create(**validated_data)
        """Create a new post and return it."""
        tags = validated_data.pop('tags', [])
        service_requested = validated_data.pop('service_requested', [])
        post = Post.objects.create(**validated_data)
        self._get_or_create_tag(tags, post)
        self._get_or_create_service_requested(service_requested, post)

        return post

    def update(self, instance, validated_data):
        """Update a post and return it."""
        tags = validated_data.pop('tags', None)
        service_requested = validated_data.pop('service_requested', None)
        print('service_requested', service_requested)
        print('tags', tags)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tag(tags, instance)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail"""
    post_service_events = servicesSerializers.PostServiceEventsSerializer(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        # fields = PostSerializer.Meta.fields + ['description', 'link', 'image']
        fields = PostSerializer.Meta.fields + ['description', 'link', 'image', 'post_service_events']


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to posts"""

    class Meta:
        model = Post
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image': {'required': True}
        }
