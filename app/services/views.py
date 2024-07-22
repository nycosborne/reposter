""" Views for the social account services. """
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from services.linkedinAPI import LinkedInAPI
from services.redditAPI import RedditAPI

from core.models import SocialAccounts, PostServiceEvents

from services import serializers as servicesSerializers
from post import serializers as postSerializers


class PostServiceEventsViewSet(viewsets.ModelViewSet):
    """Manage post service events in the database."""
    serializer_class = servicesSerializers.PostServiceEventsSerializer
    queryset = PostServiceEvents.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user)


class SocialAccountsViewSet(viewsets.ModelViewSet):
    """Manage social accounts in the database."""
    serializer_class = servicesSerializers.SocialAccountsSerializer
    queryset = SocialAccounts.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ReceivingCode(APIView):
    # TODO:Need to research if linkedin_api.get_access_token(code)
    #  should be called in the serializer or here
    serializer_class = servicesSerializers.CodeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            auth_user = request.user
            # request = self.request
            print(f"ReceivingCode.post request: {serializer.data}")
            if serializer.data['account_type'] == 'linkedin':
                linkedin_api = LinkedInAPI(auth_user, serializer.data)
                code = serializer.data['code']
                linkedin_api.get_access_token(code)
            if serializer.data['account_type'] == 'reddit':
                print("CodeSerializer.reddit")
                reddit_api = RedditAPI(auth_user, serializer.data)
                code = serializer.data['code']
                reddit_api.get_access_token(code)

            return Response({"message": "Toke received successfully."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def standerdize_post_service_events(data):
    """Standerdize post_service_events."""
    post_service_events = []
    index = 0

    while True:
        service_key = f'post_service_events[{index}][service]'
        status_key = f'post_service_events[{index}][status]'

        if service_key in data and status_key in data:
            post_service_events.append({
                'service': data.get(service_key),
                'status': data.get(status_key)
            })
            index += 1
        else:
            break

    return post_service_events


class PostToSocialAccounts(APIView):
    post_serializers_class = postSerializers.PostDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"PostToSocialAccounts.post request.data: {request.data}")
        post_serializer = self.post_serializers_class(data=request.data)
        # value, key, posted_to, posted = None
        if post_serializer.is_valid():
            # array to select which service to post
            post_service_events = standerdize_post_service_events(request.data)

            for post_service_event in post_service_events:
                if (post_service_event['service'] == 'linkedin' and
                        post_service_event['status'] == 'SET_TO_PUBLISH'):
                    print("Processing LinkedIn service")
                    print(f"Request.data: {request.data}")
                    print(f"post_serializer.data: {post_serializer.data}")
                    linkedin_api = LinkedInAPI(request.user, request)
                    linkedin_api.post_image_to_linkedin(
                        post_serializer.data, request.data['id'])

                if (post_service_event['service'] == 'reddit' and
                        post_service_event['status'] == 'SET_TO_PUBLISH'):
                    print("Processing Reddit service")
                    reddit_api = RedditAPI(request.user, request)
                    reddit_api.post_to_reddit(
                        post_serializer.data, request.data['id'])
                    # TODO: need to handle update response
                    # posted = reddit_api.post_to_reddit(
                    #     post_serializer.data, request.data['id'])
                    # posted_to = 'Reddit'

            return Response({
                "message": f"Post ID {request.data.get('title')}",
                "error": post_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        print('Error:', post_serializer.errors)
        return Response(f"Validation failed: {post_serializer.errors}",
                        status=status.HTTP_400_BAD_REQUEST)
