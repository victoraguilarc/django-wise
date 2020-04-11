# -*- coding: utf-8 -*-

from django.db import migrations
from django.conf import settings


def update_site_forward(apps, schema_editor):
    """Set web domain and name."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            'domain': 'https://xiberty.com',
            'name': 'Sawi'
        }
    )


def update_site_backward(apps, schema_editor):
    """Revert web domain and name to default."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            'domain': 'xiberty.com',
            'name': 'xiberty.com'
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
