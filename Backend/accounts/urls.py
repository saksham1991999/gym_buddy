from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'accounts'

router = DefaultRouter()
router.register('users', views.UserAPIView, basename='users')


urlpatterns = [
    path("", include(router.urls)),
]