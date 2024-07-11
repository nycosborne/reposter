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


class PostToSocialAccounts(APIView):
    print("PostToSocialAccounts")
    serializer_class = postSerializers.PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(request.data)
            for item in request.data:
                if item['service'] == 'linkedin':
                    print("linkedin")
                    linkedin_api = LinkedInAPI(request.user, request)
                    posted = linkedin_api.post_to_linkedin(
                        serializer.data, request.data['post_id'])

                    if posted:
                        # Update the status of the post
                        # Update the status of the post_service_event
                        return Response({
                            "message": f"post ID: {request.data['post_id']}"
                                       f" Successfully posted to LinkedIn."},
                            status=status.HTTP_201_CREATED)

                if item['service'] == 'reddit':
                    print("Reddit")
                    reddit_api = RedditAPI(request.user, request)
                    posted = reddit_api.post_to_reddit(serializer.data,
                                                       request.data['post_id'])

                    if posted:
                        return Response({
                            "message": f"post ID: {request.data['post_id']}"
                                       f" Successfully posted to Reddit."},
                            status=status.HTTP_201_CREATED)

                    return Response(
                        {"message": f"post ID {request.data['post_id']}",
                         "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

        #     if request.data['service_requested'] == 'linkedin':
        #         linkedin_api = LinkedInAPI(request.user, request)
        #         posted = linkedin_api.post_to_linkedin(serializer.data,
        #                                                request.data['post_id'])
        #
        #         if posted:
        #             return Response({
        #                 "message": f"post ID: {request.data['post_id']}"
        #                            f" Successfully posted to LinkedIn."},
        #                 status=status.HTTP_201_CREATED)
        #
        #     if request.data['service_requested'] == 'reddit':
        #         print("Reddit")
        #         reddit_api = RedditAPI(request.user, request)
        #         posted = reddit_api.post_to_reddit(serializer.data,
        #                                            request.data['post_id'])
        #
        #         if posted:
        #             return Response({
        #                 "message": f"post ID: {request.data['post_id']}"
        #                            f" Successfully posted to Reddit."},
        #                 status=status.HTTP_201_CREATED)
        #
        # return Response({"message": f"post ID {request.data['post_id']}",
        #                  "error": serializer.errors},
        #                 status=status.HTTP_400_BAD_REQUEST)
