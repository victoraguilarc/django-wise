# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.accounts.selectors.user_selector import UserSelector
from apps.accounts.services.session_service import SessionService
from apps.accounts.serializers.login_serializer import LoginSerializer
from apps.accounts.serializers.session_serializer import SessionSerializer, AccessTokenSerializer, GoogleTokenSerializer


class GoogleLoginView(APIView):
    """Process a google token_id login."""

    def post(self, request):
        """Get session from google token id.

        POST /api/v1/auth/google-login/
        """
        serializer = GoogleTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = SessionService.process_google_token(
            serializer.validated_data['token'],
        )

        return Response(SessionSerializer(user).data)


class FacebookLoginView(APIView):
    """Process Login with Facebook Access Token."""

    def post(self, request):
        """Get session from facebook access token.

        POST /api/v1/auth/facebook-login/
        """
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = SessionService.process_facebook_token(
            serializer.validated_data['access_token'],
        )

        return Response(SessionSerializer(user).data)


class LoginView(APIView):
    """Process a google token_id login."""

    def post(self, request):
        """Get session from google token id.

        POST /api/v1/auth/login/
        """
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data.get('user')
        plain_password = serializer.validated_data.get('password')

        user = UserSelector.get_by_username_or_email(username_or_email)
        SessionService.validate_session(user, plain_password)

        return Response(SessionSerializer(user).data)
