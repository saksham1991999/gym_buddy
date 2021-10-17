import os, django
import random
from faker import Faker

from accounts.models import User
from datetime import datetime
from django.contrib.gis.geos import GEOSGeometry

fake = Faker()
Faker.seed(999)


def populate_users(N):
    longitude = random.uniform(76, 78)
    latitude = random.uniform(28, 29)
    user = User.objects.create_superuser(
        username='9999999999', password="admin",  first_name="Saksham", last_name="Mittal", dob=datetime.now(), gender="M",
        city="Delhi", profile_pic=f'users/({fake.random_int(min=1, max=200)}).png',
        last_location = GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
    )
    # for _ in range(2):
    #     add_superuser()
    for _ in range(N):
        add_user()


def add_superuser():
    username = fake.random_number(digits=10)
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = fake.password(length=12)
    user = User.objects.create_superuser(username=username, first_name=first_name, last_name=last_name, password="admin",
                                         profile_pic=f'users/({fake.random_int(min=1, max=200)}).png',)


def add_user():
    username = fake.random_number(digits=10)
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = fake.password(length=12)
    longitude = random.uniform(76, 78)
    latitude = random.uniform(28, 29)
    user = User.objects.create_user(
        username=username,
        email=fake.email(),
        first_name=first_name,
        last_name=last_name,
        password=password,
        gender=fake.random_element(elements = ("M", "F")),
        type=fake.random_element(elements = ("U", "T")),
        profile_pic=f'users/({fake.random_int(min=1, max=200)}).png',
        city="Delhi",
        dob=fake.date_of_birth(minimum_age=16),
        last_location=GEOSGeometry('SRID=4326;POINT(' + str(longitude) + ' ' + str(latitude) + ')')
    )
    user.save()