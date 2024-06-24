""" URLS for the post app """

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from services import views

# Generates the URL patterns for the viewset
router = DefaultRouter()
# Register the viewset with the router
router.register('services', views.SocialAccountsViewSet)

app_name = 'services'

urlpatterns = [
    path('', include(router.urls)),
]
