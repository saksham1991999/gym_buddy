from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .choices import GENDER_CHOICES, USER_TYPE_CHOICES


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to="user-profile-pics", blank=True, null=True)

    current_gym = models.ForeignKey("center.Center", on_delete=models.SET_NULL, null=True, blank=True)

    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    dob = models.DateField()
    city = models.CharField(max_length=64)
    last_location = models.PointField(max_length=40, null=True)
    preferred_radius = models.IntegerField(default=5,
                                           help_text="in kilometers")
    type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default="U")

    active = models.BooleanField(default=True)