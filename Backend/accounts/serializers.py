from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
import random

from .models import User, UserInterest


class CustomRegisterSerializer(RegisterSerializer):
    # referral_code = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)
    profile_pic = serializers.ImageField()
    gender = serializers.CharField()
    dob = serializers.DateField(input_formats=['iso-8601'])

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'profile_pic', 'gender', 'dob')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'profile_pic': self.validated_data.get('profile_pic', ''),
            'gender': self.validated_data.get('gender', ''),
            'dob': self.validated_data.get('dob', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        print(self.cleaned_data)
        print(request)
        user.gender = self.cleaned_data.get('gender')
        user.dob = self.cleaned_data.get('dob')
        # referral_code = self.cleaned_data.get('referral_code')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    profile_pic = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user', 'username', 'profile_pic', 'first_name', 'last_name')

    def get_username(self, obj):
        return obj.user.username

    def get_profile_pic(self, obj):
        if obj.user.profile_pic:
            return obj.user.profile_pic.url
        return None

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name


class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ("id", "title", "image", "description")


class UserDistanceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(
    )
    user_interests = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            "profile_pic",
            "gender",
            "dob",
            "city",
            "type",
            "active",
            "distance",
            "user_interests",
        )

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return str(obj.distance)
        else:
            return None

    def get_user_interests(self, obj):
        queryset = obj.interests
        serializer = UserInterestSerializer(queryset, many=True)
        return serializer.data


class UserListSerializer(serializers.ModelSerializer):
    user_interests = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            "profile_pic",
            "gender",
            "dob",
            "city",
            "type",
            "active",
        )

    def get_user_interests(self, obj):
        serializer = UserInterestSerializer(obj.interests.all())
        return serializer.data


class UserDetailSerializer(serializers.ModelSerializer):
    user_interests = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            "profile_pic",
            "gender",
            "dob",
            "city",
            "last_location",
            "preferred_radius",
            "type",
            "active",
            "user_interests",
        )

    def get_user_interests(self, obj):
        serializer = UserInterestSerializer(obj.interests.all())
        return serializer.data
