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

from core.models import SocialAccounts
from services import serializers as servicesSerializers
from post import serializers as postSerializers


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
            serializer.save()
            return Response({"message": "Toke received successfully."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostToSocialAccounts(APIView):
    serializer_class = postSerializers.PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(request.data)
            if request.data['social_accounts'] == 'linkedin':
                linkedin_api = LinkedInAPI(request.user, request)
                posted = linkedin_api.post_to_linkedin(serializer.data,
                                                       request.data['post_id'])

                if posted:
                    return Response({
                        "message": f"post ID: {request.data['post_id']}"
                                   f" Successfully posted to LinkedIn."},
                        status=status.HTTP_201_CREATED)

            if request.data['social_accounts'] == 'reddit':
                print("Reddit")
                reddit_api = RedditAPI(request.user, request)
                posted = reddit_api.post_to_reddit(serializer.data,
                                                   request.data['post_id'])

                if posted:
                    return Response({
                        "message": f"post ID: {request.data['post_id']}"
                                   f" Successfully posted to Reddit."},
                        status=status.HTTP_201_CREATED)

        return Response({"message": f"post ID {request.data['post_id']}",
                         "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
