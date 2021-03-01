from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from users.models import User
from users.utils import validate_passwords


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def update(self, instance, validated_data):
        # delete previous avatar before uploading new one
        if 'avatar' in validated_data:
            instance.avatar.delete(save=False)
        instance = super(UserSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = User
        fields = ['url', 'username', 'avatar', 'first_name', 'last_name', 'email', 'about']
        read_only_fields = ['url', 'username']


class RegistrationSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        style={
            'input_type': 'password',
            'placeholder': _('password'),
        },
        required=True,
        write_only=True,
        validators=[password_validation.validate_password]
    )
    password_confirmed = serializers.CharField(
        style={
            'input_type': 'password',
            'placeholder': _('confirm password'),
        },
        required=True,
        write_only=True,
    )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmed = attrs.pop('password_confirmed')
        validate_passwords(password, password_confirmed)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
        )
        user.save()

        return user

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'about', 'password', 'password_confirmed']
        read_only_fields = ['url', 'first_name', 'last_name', 'about']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        style={
            'placeholder': _('username'),
        },
        max_length=150,
        required=True,
        write_only=True,
        validators=[UnicodeUsernameValidator()]
    )
    password = serializers.CharField(
        style={
            'input_type': 'password',
            'placeholder': _('password'),
        },
        required=True,
        write_only=True,
        validators=[password_validation.validate_password]
    )

    def validate(self, attrs):
        request = self.context['request']
        if request.user.is_authenticated:
            raise ValidationError(_("Already logged in."))
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValidationError({'password': _("Wrong username or password.")})
        attrs['user'] = user
        return attrs
