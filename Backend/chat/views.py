from functools import reduce

from django.shortcuts import render
from django.utils import tree
from rest_framework import permissions

from rest_framework import serializers, viewsets, status
from rest_framework.views import APIView
from django.contrib.postgres.search import TrigramSimilarity

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Room, RoomUser
from chat.serializers import MessageSerializer, RoomSerializer, RoomListSerializer, \
    RoomUserSerializer, \
    RoomLastMessageSerializer, Message

from django.db.models import Q, F
import operator

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from accounts.models import User
from accounts.serializers import UserListSerializer


class RoomViewset(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        rooms = Room.objects.filter(users=self.request.user, room_users__role__in=["A", "U"],
                                    room_users__left_at=None, deleted_at=None)
        return rooms

    def list(self, request):
        queryset = self.get_queryset()
        context = {'request': request}
        serializer = RoomListSerializer(queryset, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, format=None):
        users = request.data.get("users", None)
        if users:
            users = list(set(map(int, users.strip().strip(",").split(","))))
            if len(users) > 1:
                serializer = RoomSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    room_user = RoomUser.objects.create(user=request.user, room_id=serializer.data['id'], role="A")
                    RoomUser.objects.bulk_create(
                        [
                            RoomUser(user_id=user, room_id=serializer.data['id'], role="U")
                            for user in users
                        ]
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No User Selected"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], name='Add Users to a Group')
    def add_users(self, request, format=None):
        room = self.get_object()
        users = request.data.get("users", None)
        if users:
            users = list(set(map(int, users.strip().strip(",").split(","))))
            RoomUser.objects.bulk_create(
                [
                    RoomUser(user_id=user, room=room, role="U")
                    for user in users
                ]
            )
            return Response({"success": "Users Added"}, status=status.HTTP_200_OK)
        return Response({"error": "No User Selected"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete', 'get'], name='Remove a User from Group',
            permission_classes=[IsAuthenticated])
    def remove_user(self, request, pk=None):
        room = self.get_object()
        user_to_be_removed_id = request.data.get("roomuser_id", None)
        user_remover = RoomUser.objects.get(room=room, user=request.user)
        if user_remover.role == 'A':
            RoomUser.objects.get(room=room, id=user_to_be_removed_id).delete()
            return Response({"success": "User deleted"}, status=status.HTTP_200_OK)
        return Response({"error": "User is not admin"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete', 'get'], name='leave-group', permission_classes=[IsAuthenticated])
    def leave_group(self, request, pk=None):
        room = self.get_object()
        user_to_leave = RoomUser.objects.get(room=room, user=request.user)
        RoomUser.objects.get(room=room, user__id=request.user.id).delete()
        return Response({"success": "User left"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete', 'get'], name='make-admin', permission_classes=[IsAuthenticated])
    def make_Admin(self, request, pk=None):
        user_to_become_admin = request.data.get("roomuser_id", None)  # id of user to become admin
        room = self.get_object()
        user_admin_maker = RoomUser.objects.get(room=room, user=request.user)
        if user_admin_maker.role == 'A':
            if user_to_become_admin.role == 'A':
                return Response({"success": "User is already admin"}, status=status.HTTP_400_BAD_REQUEST)
            user_to_become_admin = RoomUser.objects.get(room=room, id=user_to_become_admin)
            user_to_become_admin.role = 'A'
            user_to_become_admin.save()
            return Response({"success": "User is now admin"}, status=status.HTTP_200_OK)
        RoomUser.objects.get(room=room, user__id=request.user.id).delete()
        return Response({"success": "Failed"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], name='last-message')
    def last_message(self, request, pk=None):
        context = {
            "request": request,
        }
        queryset = self.get_queryset()
        serializer = RoomLastMessageSerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], name='room-users')
    def users(self, request, pk=None):
        users = RoomUser.objects.filter(room__id=pk)
        context = {'request': request}
        serializer = RoomUserSerializer(users, many=True, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], name='chats')
    def chats(self, request, pk=None):
        room = self.get_object()
        messages = Message.objects.filter(room=room).order_by("created_on")
        context = {'request': request}
        serializer = MessageSerializer(messages, many=True, context=context)
        return Response(serializer.data)