from django.contrib.auth import password_validation
from rest_framework import serializers

from users.models import User
from users.utils import validate_passwords


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        required=True,
        write_only=True,
    )
    password_confirmed = serializers.CharField(
        style={'input_type': 'password'},
        required=True,
        write_only=True,
    )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmed = attrs.pop('password_confirmed')
        validate_passwords(password, password_confirmed)
        return attrs

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.pop('username'),
                                        email=validated_data.pop('email'),
                                        password=validated_data.pop('password'),
                                        phone_number=validated_data.pop('phone_number'))
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'password_confirmed']
        read_only_fields = ['id']
