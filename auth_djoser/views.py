from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from rest_framework import generics, permissions, status, response, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.tokens import default_token_generator
from . import serializers, settings, utils, signals

from user.models import UserProfile
from datetime import datetime

User = get_user_model()


class RootView(views.APIView):
    """
    Root endpoint - use one of sub endpoints.
    """
    permission_classes = (
        permissions.AllowAny,
    )
    urls_mapping = {
        'me': 'user',
        'register': 'register',
        'activate': 'activate',
        'change-' + User.USERNAME_FIELD: 'set_username',
        'change-password': 'set_password',
        'password-reset': 'password_reset',
        'password-reset-confirm': 'password_reset_confirm',
        'login': 'login',
        'logout': 'logout'
    }
    urls_extra_mapping = None

    def get_urls_mapping(self, **kwargs):
        mapping = self.urls_mapping.copy()
        mapping.update(kwargs)
        if self.urls_extra_mapping:
            mapping.update(self.urls_extra_mapping)
        mapping.update(settings.get('ROOT_VIEW_URLS_MAPPING'))
        return mapping

    def get(self, request, format=None):
        return Response(
            dict([(key, reverse(url_name, request=request, format=format))
                  for key, url_name in self.get_urls_mapping().items()])
        )


class RegistrationView(utils.SendEmailViewMixin, generics.CreateAPIView):
    """
    Use this endpoint to register new user.
    """
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator
    subject_template_name = 'activation_email_subject.txt'
    plain_body_template_name = 'activation_email_body.txt'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.perform_create(serializer):
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response('Missing arguments for UserProfile', status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        key_set = set([x for x in self.request.data.keys()])
        if not {'displayName', 'isCoach', 'city'}.issubset(key_set):
            return False
        profile_data = {}
        for k in key_set:
            if k in {'displayName', 'isCoach', 'city', 'birthdate', 'description'}:
                profile_data[k] = self.request.data[k]
        print(profile_data)
        u = serializer.save()
        up = UserProfile.objects.create(user=u, **profile_data)
        try:
            levels = self.request.data['levels']
            up.levels = levels
        except KeyError:
            pass
        up.user = u
        up.save()
        return True

    def get_email_context(self, user):
        context = super(RegistrationView, self).get_email_context(user)
        context['url'] = settings.get('ACTIVATION_URL').format(**context)
        return context


class LoginView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """
    serializer_class = serializers.LoginSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def action(self, serializer):
        user = serializer.user
        token, _ = Token.objects.get_or_create(user=user)
        user_logged_in.send(sender=user.__class__, request=self.request, user=user)
        return Response(
            data=serializers.TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )


class LogoutView(views.APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return response.Response(status=status.HTTP_200_OK)


class PasswordResetView(utils.ActionViewMixin, utils.SendEmailViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to send email to user with password reset link.
    """
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator
    subject_template_name = 'password_reset_email_subject.txt'
    plain_body_template_name = 'password_reset_email_body.txt'

    def action(self, serializer):
        for user in self.get_users(serializer.data['email']):
            self.send_email(**self.get_send_email_kwargs(user))
        return response.Response(status=status.HTTP_200_OK)

    def get_users(self, email):
        active_users = User._default_manager.filter(
            email__iexact=email,
            is_active=True,
        )
        return (u for u in active_users if u.has_usable_password())

    def get_email_context(self, user):
        context = super(PasswordResetView, self).get_email_context(user)
        context['url'] = settings.get('PASSWORD_RESET_CONFIRM_URL').format(**context)
        return context


class SetPasswordView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to change user password.
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_serializer_class(self):
        if settings.get('SET_PASSWORD_RETYPE'):
            return serializers.SetPasswordRetypeSerializer
        return serializers.SetPasswordSerializer

    def action(self, serializer):
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()
        return response.Response(status=status.HTTP_200_OK)


class PasswordResetConfirmView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to finish reset password process.
    """
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def get_serializer_class(self):
        if settings.get('PASSWORD_RESET_CONFIRM_RETYPE'):
            return serializers.PasswordResetConfirmRetypeSerializer
        return serializers.PasswordResetConfirmSerializer

    def action(self, serializer):
        serializer.user.set_password(serializer.data['new_password'])
        serializer.user.save()
        return response.Response(status=status.HTTP_200_OK)


class ActivationView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to activate user account.
    """
    serializer_class = serializers.ActivationSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def action(self, serializer):
        serializer.user.is_active = True
        serializer.user.save()
        signals.user_activated.send(
            sender=self.__class__, user=serializer.user, request=self.request)
        return Response(status=status.HTTP_200_OK)


class SetUsernameView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to change user username.
    """
    serializer_class = serializers.SetUsernameSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_serializer_class(self):
        if settings.get('SET_USERNAME_RETYPE'):
            return serializers.SetUsernameRetypeSerializer
        return serializers.SetUsernameSerializer

    def action(self, serializer):
        setattr(self.request.user, User.USERNAME_FIELD, serializer.data['new_' + User.USERNAME_FIELD])
        self.request.user.save()
        return response.Response(status=status.HTTP_200_OK)


class UserView(generics.RetrieveUpdateAPIView):
    """
    Use this endpoint to retrieve/update user.
    """
    model = User
    serializer_class = serializers.UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_object(self, *args, **kwargs):
        return self.request.user
