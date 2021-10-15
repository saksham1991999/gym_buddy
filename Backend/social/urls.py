from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'social'

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('likes', views.PostReactViewSet, basename='likes')
router.register('comments', views.PostCommentViewSet, basename='comments')
router.register('replies', views.PostCommentReplyViewSet, basename='replies')


urlpatterns = [
    path("", include(router.urls)),
    path("followers/", views.FollowersListAPIView.as_view()),
    path("following/", views.FollowingListAPIView.as_view()),
]
