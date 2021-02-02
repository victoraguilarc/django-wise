# -*- coding: utf-8 -*-

import factory
from faker import Factory
from faker.providers import misc, person, profile

from apps.accounts.models.user import User

fake = Factory.create()
fake.add_provider(person)
fake.add_provider(profile)
fake.add_provider(misc)


def fake_username():
    return fake.simple_profile()['username']


def generate_user_profile():
    user_profile = fake.simple_profile()
    user_password = fake.uuid4()
    full_name = fake.name().split(' ')
    return {
        'username': user_profile['username'],
        'email': user_profile['mail'],
        'firstName': full_name[0],
        'lastName': full_name[1],
        'password': user_password,
    }


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.LazyFunction(fake_username)
    email = factory.LazyFunction(fake.email)
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)

    class Meta:
        model = User
