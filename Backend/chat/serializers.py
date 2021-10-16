from django.db import models
from rest_framework import serializers

from .models import Room, RoomUser, Message, ReportGroup
from accounts.serializers import UserListSerializer


class RoomSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "title",
            "description",
            "image",
            "created_at",
            "deleted_at",
        ]


class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "title",
            "image",
        ]


class RoomLastMessageSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField(read_only=True)
    unseen_messages = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "title",
            "image",
            "last_message",
            "unseen_messages",
            "is_admin",
        ]

    def get_last_message(self, obj):
        message = Message.objects.filter(room=obj).first()
        serializer = MessageSerializer([message], many=True)
        return serializer.data

    def get_unseen_messages(self, obj):
        request = self.context.get('request', None)
        user = request.user
        if user:
            room_user = RoomUser.objects.get(user=user, room=obj)
            messages = Message.objects.filter(room=obj, created_on__gte=room_user.viewed_at)
            if messages.exists():
                return messages.count()
        return None

    def get_is_admin(self, obj):
        request = self.context.get("request", None)
        user = request.user
        return True


class RoomUserSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    user = UserListSerializer()
    joined_at = serializers.ReadOnlyField()

    class Meta:
        model = RoomUser
        fields = [
            "id",
            "user",
            "role",
            "joined_at",
            "left_at"
        ]


class MessageSerializer(serializers.ModelSerializer):
    file_field = serializers.FileField(allow_empty_file = True)
    created_on = serializers.SerializerMethodField(read_only=True)
    user = UserListSerializer()
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "type",
            "file_field",
            "message_text",
            "user",
            "created_on",
            "room"
        ]

    @staticmethod
    def get_type(self):
        return "send_to_websocket"

    def get_created_on(self, obj):
        return obj.created_on.strftime("%d %b %Y %H:%M:%S %Z")


class ReportGroupSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ReportGroup
        fields = ['id', 'user', 'room', 'date_time']