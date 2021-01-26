# -*- coding: utf-8 -*-

import factory
from faker import Factory
from factory.fuzzy import FuzzyChoice
from faker.providers import misc, lorem

from apps.accounts.models.choices import Platform
from apps.accounts.models.phone_device import PhoneDevice

faker = Factory.create()
faker.add_provider(misc)
faker.add_provider(lorem)


class PhoneDeviceFactory(factory.django.DjangoModelFactory):
    token = factory.LazyFunction(faker.sha256)
    platform = FuzzyChoice(choices=Platform.values())
    model_name = factory.LazyFunction(faker.word)

    class Meta:
        model = PhoneDevice
