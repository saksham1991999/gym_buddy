from rest_framework import serializers
import random

from .models import CenterType, Center, CenterImages


class CenterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterType
        fileds = "__all__"


class CenterDistanceSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    latitude = serializers.SerializerMethodField(read_only=True)
    longitude = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Center
        fields = ('id', 'type', 'name', 'location', 'city', "latitude", "longitude")

    @staticmethod
    def get_images(obj):
        images = CenterImages.objects.filter(center=obj)
        serializer = CenterImageSerializer(images, many=True)
        return serializer.data

    @staticmethod
    def get_latitude(obj):
        if obj.last_location:
            return obj.last_location.x
        return None

    @staticmethod
    def get_longitude(obj):
        if obj.last_location:
            return obj.last_location.y
        return None


class CenterListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Center
        fields = ('id', 'type', 'name', 'location', 'city')

    def get_images(self, obj):
        images = CenterImages.objects.filter(center=obj)
        serializer = CenterImageSerializer(images, many=True)
        return serializer.data


class CenterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = "__all__"


class CenterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterImages
        fields = ('image')