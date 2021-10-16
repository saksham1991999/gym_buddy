import os, django

from faker import Faker

from accounts.models import User
from datetime import datetime

fake = Faker()
Faker.seed(999)


def populate_users(N):
    user = User.objects.create_superuser(
        username='9999999999', password="admin",  first_name="Saksham", last_name="Mittal", dob=datetime.now(), gender="M",
        city="Delhi", profile_pic=f'users/({fake.random_int(min=1, max=200)}).png'
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
    add_addresses(user)


def add_addresses(user):
    # user = User.objects.create_user(username='8888888888', password="admin")
    # user = User.objects.create_user(username='7777777777', password="admin")
    # user = User.objects.create_user(username='6666666666', password="admin")
    Address.objects.bulk_create(
        [
            Address(
                user=user,
                full_name=fake.name(),
                street_address_1=fake.building_number(),
                street_address_2=fake.street_name(),
                city=fake.city(),
                state=fake.street_suffix(),
                postal_code=fake.postcode(),
                phone=fake.random_number(digits=10, fix_len=True))
            for _ in range(fake.random_int(min=2, max=10))
        ]
    )


def add_user():
    username = fake.random_number(digits=10)
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = fake.password(length=12)
    user = User.objects.create_user(
        username=username,
        email=fake.email(),
        first_name=first_name,
        last_name=last_name,
        password=password,
        gender=fake.random_element(elements = ("M", "F")),
        profile_pic=f'users/({fake.random_int(min=1, max=200)}).png',
        city="Delhi",
        dob=fake.date_of_birth(minimum_age=16)
    )
    user.save()