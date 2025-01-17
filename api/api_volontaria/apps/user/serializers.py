from datetime import datetime
import re

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.db.models.fields import DurationField
from django.utils.translation import gettext_lazy as _

from rest_framework.settings import api_settings

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from dry_rest_permissions.generics import DRYGlobalPermissionsField
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import PasswordResetSerializer

from api_volontaria.apps.user.models import ActionToken
from api_volontaria.apps.user.models import APIToken

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):

    first_name = serializers.CharField(
        max_length=30,
        allow_blank=True,
        allow_null=True,
        required=False
    )

    last_name = serializers.CharField(
        max_length=150,
        allow_blank=True,
        allow_null=True,
        required=False
    )

    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def validate(self, data):
        if 'password1' in data and data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password didn't match."))

        return data


class CustomPasswordResetSerializer(PasswordResetSerializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def save(self):

        try:
            from api_volontaria.apps.notification.models import Notification
            Notification.generate_reset_password(
                User.objects.get(
                    email=self.validated_data.get('email')
                )
            )
        except ObjectDoesNotExist:
            pass


class UserSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()
    permissions = DRYGlobalPermissionsField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'help_text': _("A valid password."),
            },
            'first_name': {
                'allow_blank': False,
                'help_text': _("A valid first name."),
            },
            'last_name': {
                'allow_blank': False,
                'help_text': _("A valid last name."),
            },
        }
        read_only_fields = (
            'id',
            'url',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
            'last_login',
            'groups',
            'user_permissions',
            'email',
            'permissions'
        )


class UserLightSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'first_name',
            'last_name',
            'email',
        ]
        read_only_fields = (
            'id',
            'url',
            'first_name',
            'last_name',
            'email',
        )


class APITokenSerializer(serializers.Serializer):
    ''' Class strongly inspired from AuthTokenSerializer class 
    in Django Rest Framework.
    Additions: the fields 'purpose' and 'user_email' 
    (unlike in DRF AuthTokenSerializer,
    the user associated with the token is not always
    the user issuing the request (rarely in fact)
    )
    Note: 
    We do not subclass ModelSerializer because:
    1. The serializer needs read and write access
        to the field user_email,
        which is not a field in the APIToken model
        (but a User field, user being a foreign key in APIToken model)
    2. We do not want an update method
    '''
    # dry_rest_framework requires Serializer class to have Meta attribute
    class Meta:
       model = APIToken

    purpose = serializers.CharField(
        label=_("Purpose"),
    )

    user_email = serializers.EmailField(
        label=_("User_email"),
    )

    token = serializers.CharField(
        label=_("APIToken"),
        read_only=True
    )
