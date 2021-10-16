from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'accounts'

router = DefaultRouter()
router.register("rooms", views.RoomViewset, basename="rooms")


urlpatterns = [
    path("", include(router.urls)),
]