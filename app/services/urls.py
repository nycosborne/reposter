""" URLS for the post app """

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from services import views

# Generates the URL patterns for the viewset
router = DefaultRouter()
# Register the viewset with the router
router.register('services', views.PostServiceEventsViewSet,
                basename='services')

app_name = 'services'

urlpatterns = [
    path('', include(router.urls)),
    path('passcode/', views.ReceivingCode.as_view(), name='passcode'),
    path('soc-post/', views.PostToSocialAccounts.as_view(), name='post'),
]
