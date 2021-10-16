from rest_framework import serializers
import random

from .models import CenterType, Center, CenterImages


class CenterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterType
        fileds = "__all__"


class CenterListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Center
        fields = ('id', 'type', 'name', 'location', 'city')

    def get_images(self, obj):
        images = CenterImages.objects.filter(center=obj)
        serializer = CenterImageSerializer(images, many=True)
        return serializer.data


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = "__all__"


class CenterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterImages
        fields = ('image')