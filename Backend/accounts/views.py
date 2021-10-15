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

from .serializers import UserListSerializer, UserDetailSerializer
from .models import User
from social.models import Follower


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

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated, ], name="Nearby Groups")
    def groups_nearby(self, request, *args, **kwargs):
        # longitude = request.data['long']
        # latitude = request.data['lat']
        rooms = Room.objects.all()[:20]
        serializer = RoomListSerializer(rooms, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated, ], name="Follow User")
    def follow(self, request, *args, **kwargs):
        user_id = request.data["user"]
        user = get_object_or_404(User, id=user_id)
        follow_qs = Follower.objects.get_or_create(user=user, follower=request.user)
        return Response({"success": "User Followed"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated, ], name="Unfollow User")
    def unfollow(self, request, *args, **kwargs):
        user_id = request.data["user"]
        user = get_object_or_404(User, id=user_id)
        follow_qs = get_object_or_404(Follower, user=user, follower=request.user)
        follow_qs.delete()
        return Response({"success": "User Un-Followed"}, status=status.HTTP_200_OK)

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
