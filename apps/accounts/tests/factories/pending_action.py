# -*- coding: utf-8 -*-

import factory
from faker import Factory
from factory import fuzzy
from faker.providers import misc

from apps.contrib.utils import dates
from apps.accounts.models.choices import ActionCategory
from apps.accounts.tests.factories.user import UserFactory
from apps.accounts.models.pending_action import PendingAction

faker = Factory.create()
faker.add_provider(misc)


def now_after_three():
    return dates.ago(days=3)


class PendingActionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    category = fuzzy.FuzzyChoice(choices=ActionCategory.choices())
    creation_date = factory.LazyFunction(dates.now)
    expiration_date = factory.LazyFunction(now_after_three)
    token = factory.LazyFunction(faker.uuid4)

    class Meta:
        model = PendingAction
