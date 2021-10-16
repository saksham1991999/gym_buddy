from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'center'

router = DefaultRouter()
router.register('centers', views.CenterAPIView, basename='centers')
urlpatterns = [
    path("", include(router.urls)),
]
