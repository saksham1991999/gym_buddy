from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import F, IntegerField
from django.db.models.functions import Least
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import generics, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import UserListSerializer, UserDetailSerializer
from .models import User


class UserAPIView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        if self.action == 'list':
            return UserListSerializer(*args, **kwargs)
        else:
            return UserDetailSerializer(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        latitude = self.request.query_params.get("latitude", None)
        longitude = self.request.query_params.get("longitude", None)
        if latitude and longitude:
            ref_location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
            user.last_location = ref_location
            user.save()
            queryset = User.objects.all().annotate(distance=Distance("last_location", ref_location)).order_by('distance')
        else:
            queryset = User.objects.filter(city=user.city)
        queryset = queryset.exclude(id=user.id)
        return queryset


    #     current_user_location = Point(
    #         float(self.kwargs.get('current_longitude')),
    #         float(self.kwargs.get('current_latitude')),
    #         srid=4326
    #     )
    #     # we annotate each object with smaller of two radius:
    #     # - requesting user
    #     # - and each user preferred_radius
    #     # we annotate queryset with distance between given in params location
    #     # (current_user_location) and each user location
    #     queryset = queryset.annotate(
    #         smaller_radius=Least(
    #             finder.preferred_radius,
    #             F('preferred_radius'),
    #             output_field=IntegerField()
    #         ),
    #         distance=Distance('last_location', current_user_location)
    #     ).filter(
    #         distance__lte=F('smaller_radius') * 1000
    #     ).order_by(
    #         'distance'
    #     )
    #
    #     queryset = queryset.filter(
    #         sex=finder.sex if finder.homo else finder.get_opposed_sex,
    #         preferred_sex=finder.sex,
    #         age__range=(
    #             finder.preferred_age_min,
    #             finder.preferred_age_max),
    #         preferred_age_min__lte=finder.age,
    #         preferred_age_max__gte=finder.age,
    #     ).exclude(
    #         nickname=finder.nickname
    #     )
    #     return queryset
