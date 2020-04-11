# -*- encoding: utf-8 -*-

from django.conf import settings

global_context = {
    'project_domain': settings.PROJECT_HOSTNAME,
    'project_name': settings.PROJECT_NAME,
    'project_author': settings.PROJECT_AUTHOR,
    'project_owner': settings.PROJECT_OWNER,
    'project_owner_domain': settings.PROJECT_OWNER_DOMAIN,
    'project_description': settings.PROJECT_DESCRIPTION,
    'project_support_email': settings.PROJECT_SUPPORT_EMAIL,
    'project_support_phone': settings.PROJECT_SUPPORT_PHONE,
    'project_terms_url': settings.PROJECT_TERMS_URL,

    'DEBUG': settings.DEBUG,
}


def website(request):
    """Returns common info about the website."""
    return global_context
