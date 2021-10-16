from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import F, IntegerField
from django.db.models.functions import Least
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import generics, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from .serializers import CenterDistanceSerializer, CenterDetailSerializer
from .models import Center
from .permissions import IsOwnerOrReadOnly


class CenterAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        if self.action == 'list':
            return CenterDistanceSerializer(*args, **kwargs)
        else:
            return CenterDetailSerializer(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = Center.objects.all()

        type = self.request.query_params.get("type", None)
        if type:
            queryset = queryset.filter(type=type)

        latitude = self.request.query_params.get("latitude", None)
        longitude = self.request.query_params.get("longitude", None)
        if latitude and longitude:
            ref_location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
            user.last_location = ref_location
            user.save()
            queryset = queryset.annotate(distance=Distance("point_location", ref_location)).order_by('distance')
        elif user.last_location:
            queryset = queryset.annotate(distance=Distance("point_location", user.last_location)).order_by('distance')
        return queryset