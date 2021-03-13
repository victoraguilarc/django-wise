# -*- coding: utf-8 -*-

from django.urls import path

from apps.accounts.api.v1.views.email import EmailActionsViewSet
from apps.accounts.api.v1.views.login import LoginView, GoogleLoginView, FacebookLoginView
from apps.accounts.api.v1.views.logout import LogoutView
from apps.accounts.api.v1.views.profile import ProfileViewSet
from apps.accounts.api.v1.views.password import PasswordActionsViewSet
from apps.accounts.api.v1.views.register import RegisterView
from apps.accounts.api.v1.views.phone_verification import PhoneVerification

app_name = 'accounts'
urlpatterns = [
    # >> Register

    path(
        'auth/register/',
        RegisterView.as_view(),
        name='register',
    ),
    path(
        'auth/email/confirmation/',
        EmailActionsViewSet.as_view({'post': 'email_confirmation'}),
        name='email-confirmation',
    ),
    path(
        'auth/email/confirmation/request/',
        EmailActionsViewSet.as_view({'post': 'email_confirmation_request'}),
        name='email-confirmation-request',
    ),

    # >> Authentication
    path(
        'auth/login/',
        LoginView.as_view(),
        name='login',
    ),
    path(
        'auth/google-login/',
        GoogleLoginView.as_view(),
        name='google-login',
    ),
    path(
        'auth/facebook-login/',
        FacebookLoginView.as_view(),
        name='facebook-login',
    ),
    path(
        'auth/reset-password/',
        PasswordActionsViewSet.as_view({'post': 'reset_password'}),
        name='password-reset',
    ),
    path(
        'auth/reset-password/confirm/',
        PasswordActionsViewSet.as_view({'post': 'reset_password_confirm'}),
        name='password-reset-confirm',
    ),
    path(
        'auth/logout/',
        LogoutView.as_view(),
        name='logout',
    ),

    # >> Users

    path(
        'me/profile/',
        ProfileViewSet.as_view({'get': 'get_profile', 'put': 'update_profile'}),
        name='profile',
    ),
    path(
        'me/password/',
        PasswordActionsViewSet.as_view({'put': 'update_password', 'post': 'set_password'}),
        name='password',
    ),
    path(
        'me/phone-verification/',
        PhoneVerification.as_view(),
        name='phone-verification',
    ),
]
