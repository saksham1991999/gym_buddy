from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.db.models import Q
from rest_framework.viewsets import generics
from rest_framework.permissions import AllowAny

from social import models, serializers
from social.permissions import IsOwnerOrReadOnly
from accounts.serializers import UserListSerializer
from accounts.models import User


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     following_id = models.Follower.objects.filter(follower=self.request.user).values_list("user", flat=True)
    #     query_set = models.Post.objects.filter(user__id__in=following_id)
    #     if not query_set.exists():
    #         query_set = models.Post.objects.all()
    #     search = self.request.query_params.get('search', None)
    #     if search:
    #         query_set = query_set.filter(description__icontains=search)
    #
    #     order_by = self.request.query_params.get('orderby', None)
    #     if order_by:
    #         if order_by == "recent":
    #             query_set = query_set.orderby('-date')
    #     return query_set


class PostReactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get("post", None)
        if post_id:
            comments = models.PostLike.objects.filter(post=post_id)
            return comments
        return models.PostLike.objects.none()


class PostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostCommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get("post", None)
        if post_id:
            comments = models.PostComment.objects.filter(post=post_id)
            return comments
        return models.PostComment.objects.none()


class PostCommentReplyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostCommentReplySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        comment_id = self.request.query_params.get("comment", None)
        if comment_id:
            comments = models.PostCommentReply.objects.filter(comment=comment_id)
            return comments
        return models.PostCommentReply.objects.none()


class FollowersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer

    def get_queryset(self):
        user = self.request.user
        followers_id = models.Follower.objects.filter(user=user).values_list("follower", flat=True)
        users = get_list_or_404(User, id__in=followers_id)
        return users


class FollowingListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer

    def get_queryset(self):
        user = self.request.user
        following_id = models.Follower.objects.filter(follower=user).values_list("user", flat=True)
        users = get_list_or_404(User, id__in=following_id)
        return users