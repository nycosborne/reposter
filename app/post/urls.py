""" URLS for the post app """

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from post import views

# Generates the URL patterns for the viewset
router = DefaultRouter()
# Register the viewset with the router
router.register('post', views.PostViewSet)

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
