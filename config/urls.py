# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import path, include
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.conf.urls.static import static

from apps.contrib.views.errors import error400, error403, error404, error500

from django.contrib import admin

admin.site.site_header = 'Wise'
admin.site.site_title = 'Wise Admin'
admin.site.index_title = 'Wise Admin'

urlpatterns = [
    # Django ADMIN
    path(settings.ADMIN_URL, admin.site.urls),

    # Landing Page
    path('', TemplateView.as_view(template_name='home.html')),

    # Accounts
    path('api/', include('apps.accounts.api.urls', namespace='api-accounts')),  # api
    path('', include('apps.accounts.urls', namespace='accounts')),  # transactions
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:

    # Emails
    urlpatterns += [
        path('transactional-emails/base/', TemplateView.as_view(
            template_name='transactions/emails/base.html',
        )),

        path('transactional-emails/confirm-email/', TemplateView.as_view(
            template_name='transactions/emails/confirm_email/message.html',
        )),

        path('transactional-emails/reset-password/', TemplateView.as_view(
            template_name='transactions/emails/reset_password/message.html',
        )),
    ]

    # Pages & errors
    urlpatterns += [
        path('400/', TemplateView.as_view(template_name='errors/400.html'), name='error-400'),
        path('403/', TemplateView.as_view(template_name='errors/403.html'), name='error-403'),
        path('404/', TemplateView.as_view(template_name='errors/404.html'), name='error-404'),
        path('500/', TemplateView.as_view(template_name='errors/500.html'), name='error-500'),
    ]

    urlpatterns += [
        path('error/400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('error/403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('error/404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('error/500/', default_views.server_error),
    ]

    # Developer tools
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        if settings.DEBUG:
            import debug_toolbar  # noqa: WPS433
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
else:
    handler400 = error400
    handler403 = error403
    handler404 = error404
    handler500 = error500
